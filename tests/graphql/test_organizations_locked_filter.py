"""GraphQL coverage for VCST-5317 — the header org switcher's `GetOrganizations` query
(`me.contact.organizations`) returns every organization the caller belongs to, including
ones where their membership is currently locked, and flags each item with
`isLockedForCurrentUser` so the client can decide how to present it (the storefront renders
locked organizations as disabled rather than hiding them).

Server-side implementation (already merged, this file adds the missing regression coverage):
  - vc-module-customer: OrganizationMembership.IsCurrentlyLocked
  - vc-module-profile-experience-api: OrganizationType.isLockedForCurrentUser (batched
    per-organization flag), ContactType.organizations no longer excludes locked orgs

acme_store_employee_1 is the only seeded user with more than one organization
(organization-acme-store, organization-acme-store-2, ...), so it's used as the
locked-user fixture for every case here.
"""

from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from typing import Callable, Iterator

import allure
import pytest

from core.auth import AuthProvider
from core.clients import GraphQLClient
from core.clients.rest import RestClient
from core.global_settings import global_settings
from gql.operations import ContactOperations
from restapi.operations import ContactOperations as RestContactOperations
from tests.context import Context
from utils.polling_utils import poll_until

_USERNAME = "acme_store_employee_1@acme.com"
_ORG_TO_LOCK = "organization-acme-store-2"


def _find(items: list[dict], organization_id: str) -> dict | None:
    return next((item for item in items if item["id"] == organization_id), None)


@contextmanager
def _fresh_contact_ops(username: str) -> Iterator[ContactOperations]:
    """A locked-out membership terminates ALL of that user's sessions
    (RevokeTokenOrganizationMembershipChangedEventHandler), so the `graphql_client` fixture's
    token — issued before locking, by the `with_user` marker — is dead by the time a test
    locks its own user. Sign in fresh afterwards rather than reusing that stale client."""
    auth = AuthProvider(global_settings.backend_base_url)
    auth.sign_in(username, global_settings.users_password)
    try:
        with GraphQLClient(auth=auth, global_settings=global_settings) as client:
            yield ContactOperations(client)
    finally:
        auth.sign_out()


def _poll_organizations(
    contact_ops: ContactOperations, predicate: Callable[[tuple[int, list[dict]]], bool]
) -> tuple[int, list[dict]]:
    """isLockedForCurrentUser is batched through a DataLoader, not cached, but poll
    defensively anyway — locking itself (membership write) and the follow-up query are two
    separate requests, and this avoids coupling the test to that being instantaneous."""
    result = poll_until(
        fetch=lambda: contact_ops.get_organizations(first=200),
        predicate=predicate,
        attempts=10,
        interval=2,
    )
    return result if result is not None else contact_ops.get_organizations(first=200)


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Organizations / Locked filter (GraphQL)")
@allure.title("AC-2: GetOrganizations still returns a locked organization, flagged as locked")
def test_ac2_locked_organization_flagged(
    ctx: Context,
    graphql_client: GraphQLClient,
    lock_membership: Callable[..., None],
) -> None:
    contact_ops = ContactOperations(graphql_client)

    with allure.step(f"Baseline: fetch organizations for {_USERNAME} before locking"):
        _, baseline_items = contact_ops.get_organizations(first=200)
        baseline_org = _find(baseline_items, _ORG_TO_LOCK)
        assert baseline_org is not None, (
            f"Precondition failed: {_ORG_TO_LOCK} not present before locking — got {[i['id'] for i in baseline_items]}"
        )
        assert baseline_org["isLockedForCurrentUser"] is False

    with allure.step(f"Lock {ctx.user_name} in {_ORG_TO_LOCK}"):
        lock_membership(user_id=ctx.user_id, organization_id=_ORG_TO_LOCK)

    with allure.step("Sign in fresh (locking terminated the previous session) and poll GetOrganizations"):
        with _fresh_contact_ops(_USERNAME) as fresh_contact_ops:
            total_count, items = _poll_organizations(
                fresh_contact_ops, predicate=lambda r: (_find(r[1], _ORG_TO_LOCK) or {}).get("isLockedForCurrentUser") is True
            )

    with allure.step("Verify the org is still present, flagged as locked, and totalCount matches items[]"):
        locked_org = _find(items, _ORG_TO_LOCK)
        assert locked_org is not None, f"{_ORG_TO_LOCK} disappeared from the list: {[i['id'] for i in items]}"
        assert locked_org["isLockedForCurrentUser"] is True
        assert total_count == len(items), f"totalCount ({total_count}) != len(items) ({len(items)})"


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Organizations / Locked filter (GraphQL)")
@allure.title("AC-3: an expired timed lock is not reported as currently locked")
def test_ac3_expired_lock_not_flagged(
    ctx: Context,
    lock_membership: Callable[..., None],
) -> None:
    """Complements the unit-level coverage in vc-module-customer
    (OrganizationMembershipServiceTests.SearchAsync_OnlyLocked_ReturnsOnlyCurrentlyLocked /
    GetLockedOrganizationIdsAsync_ReturnsCurrentlyLockedOrgs) with an end-to-end check
    through the actual GetOrganizations query."""
    with allure.step(f"Lock {ctx.user_name} in {_ORG_TO_LOCK} with a lockoutEnd in the past"):
        lock_membership(
            user_id=ctx.user_id,
            organization_id=_ORG_TO_LOCK,
            lockout_end=datetime.now(timezone.utc) - timedelta(days=1),
        )

    with allure.step("Sign in fresh (locking terminated the previous session) and poll GetOrganizations"):
        with _fresh_contact_ops(_USERNAME) as fresh_contact_ops:
            _, items = _poll_organizations(
                fresh_contact_ops, predicate=lambda r: (_find(r[1], _ORG_TO_LOCK) or {}).get("isLockedForCurrentUser") is False
            )

    with allure.step("Verify the org is present and not flagged as locked"):
        org = _find(items, _ORG_TO_LOCK)
        assert org is not None, f"{_ORG_TO_LOCK} unexpectedly absent: {[i['id'] for i in items]}"
        assert org["isLockedForCurrentUser"] is False, "An expired lock must not be reported as currently locked"


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Organizations / Locked filter (GraphQL)")
@allure.title("AC-5: locking one user does not flag the organization as locked for another user")
def test_ac5_lock_isolation_between_users(
    ctx: Context,
    lock_membership: Callable[..., None],
    rest_client: RestClient,
    backend_base_url: str,
) -> None:
    """BL-B2B-001: locking user X in Org A must not change how user Y sees that org.
    acme_store_employee_2 (Y) is not seeded as a member of organization-acme-store-2, so
    it's temporarily added to their Contact.organizations (the candidate set the
    isLockedForCurrentUser resolver scopes by userId within) for this test only."""
    other_username = "acme_store_employee_2@acme.com"
    other_contact_id = "contact-acme-store-employee-2"

    rest_contact_ops = RestContactOperations(rest_client, backend_base_url)

    with allure.step(f"Add {_ORG_TO_LOCK} to {other_username}'s organizations"):
        other_contact = rest_contact_ops.get_by_id(other_contact_id)
        original_orgs = list(other_contact.model_extra.get("organizations") or [])
        if _ORG_TO_LOCK not in original_orgs:
            rest_contact_ops.update(other_contact, organizations=[*original_orgs, _ORG_TO_LOCK])

    try:
        with allure.step(f"Lock {ctx.user_name} in {_ORG_TO_LOCK}"):
            lock_membership(user_id=ctx.user_id, organization_id=_ORG_TO_LOCK)

        with allure.step(f"Verify {ctx.user_name}'s own list flags {_ORG_TO_LOCK} as locked"):
            with _fresh_contact_ops(_USERNAME) as fresh_contact_ops:
                _, items = _poll_organizations(
                    fresh_contact_ops,
                    predicate=lambda r: (_find(r[1], _ORG_TO_LOCK) or {}).get("isLockedForCurrentUser") is True,
                )
                org = _find(items, _ORG_TO_LOCK)
                assert org is not None and org["isLockedForCurrentUser"] is True

        with allure.step(f"Verify {other_username}'s list shows {_ORG_TO_LOCK} as NOT locked"):
            with _fresh_contact_ops(other_username) as other_contact_ops:
                _, other_items = other_contact_ops.get_organizations(first=200)
                other_org = _find(other_items, _ORG_TO_LOCK)
                assert other_org is not None, (
                    f"{_ORG_TO_LOCK} missing from {other_username}'s list: {[i['id'] for i in other_items]}"
                )
                assert other_org["isLockedForCurrentUser"] is False, (
                    f"Locking {ctx.user_name} in {_ORG_TO_LOCK} leaked into {other_username}'s view of it"
                )
    finally:
        with allure.step(f"Teardown: restore {other_username}'s original organizations list"):
            other_contact = rest_contact_ops.get_by_id(other_contact_id)
            rest_contact_ops.update(other_contact, organizations=original_orgs)
