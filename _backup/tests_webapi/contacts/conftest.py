import uuid
from typing import Any, Callable

import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.webapi_client import WebAPISession
from webapi_operations.contacts.contact_operations import ContactOperations
from webapi_operations.contacts.organization_operations import OrganizationOperations


# ---------------------------------------------------------------- ops fixtures


@pytest.fixture
def organization_operations(webapi_client: WebAPISession) -> OrganizationOperations:
    return OrganizationOperations(webapi_client)


@pytest.fixture
def contact_operations(webapi_client: WebAPISession) -> ContactOperations:
    return ContactOperations(webapi_client)


# ---------------------------------------------------------------- factories


@pytest.fixture
def make_organization(
    organization_operations: OrganizationOperations,
    auth: Auth,
    config: Config,
) -> Callable[..., dict]:
    """Factory that creates a fresh organization per call and cleans up at teardown.

    Usage:
        def test_x(make_organization):
            org = make_organization()                    # default name + template
            org = make_organization(name="custom")       # override name

    Authenticates once per worker (idempotent check avoids hammering /connect/token).
    Cleanup silently swallows errors so a test failure can't leak into teardown.
    """
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        if auth.token_data is None or not auth.token_data.access_token:
            auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])
        name = overrides.pop("name", f"QAOrganization_{uuid.uuid4().hex[:8]}")
        org = organization_operations.create(name=name, **overrides)
        created_ids.append(org["id"])
        return org

    yield _make

    for oid in reversed(created_ids):
        try:
            organization_operations.delete(oid)
        except Exception:
            pass


@pytest.fixture
def make_contact(
    contact_operations: ContactOperations,
    auth: Auth,
    config: Config,
) -> Callable[..., dict]:
    """Factory that creates a fresh contact per call and cleans up at teardown.

    Usage:
        def test_x(make_contact):
            contact = make_contact()
            contact = make_contact(first_name="Jane", last_name="Doe")

    Cleanup silently swallows errors so a test failure can't leak into teardown.
    """
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        if auth.token_data is None or not auth.token_data.access_token:
            auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])
        suffix = uuid.uuid4().hex[:8]
        first_name = overrides.pop("first_name", f"QAFirst_{suffix}")
        last_name = overrides.pop("last_name", f"QALast_{suffix}")
        contact = contact_operations.create(first_name=first_name, last_name=last_name, **overrides)
        created_ids.append(contact["id"])
        return contact

    yield _make

    for cid in reversed(created_ids):
        try:
            contact_operations.delete(cid)
        except Exception:
            pass
