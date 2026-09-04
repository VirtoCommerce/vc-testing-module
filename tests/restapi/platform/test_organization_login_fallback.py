"""VCST-5317 follow-up — the storefront resends the last-used organization_id on every
password sign-in (useAuth.ts), which is never a deliberate choice. If that organization (or
every organization the user belongs to) has since been locked, login must not be blocked
entirely: OrganizationIdRequestValidator.ValidateOrganizationAccessAsync drops the stale
organization_id and lets the password grant succeed without one, instead of returning
user_is_locked_in_organization.
"""

from typing import Any, Callable

import allure
import pytest
import requests

from core.global_settings import GlobalSettings

_USERNAME = "acme_store_employee_1@acme.com"


def _employee_1_organization_ids(dataset: dict[str, list[dict[str, Any]]]) -> list[str]:
    contact = next(c for c in dataset["contacts"] if c["id"] == "contact-acme-store-employee-1")
    return list(contact["organizations"])


def _employee_1_user_id(dataset: dict[str, list[dict[str, Any]]]) -> str:
    user = next(u for u in dataset["users"] if u["userName"] == _USERNAME)
    return user["id"]


@pytest.mark.restapi
@allure.feature("Platform / Organization login fallback (REST API)")
@allure.title("VCST-5317: password grant with a stale organization_id still signs in once every organization is locked")
def test_password_grant_all_organizations_locked_falls_back_and_signs_in(
    dataset: dict[str, list[dict[str, Any]]],
    lock_membership: Callable[..., None],
    global_settings: GlobalSettings,
) -> None:
    user_id = _employee_1_user_id(dataset)
    organization_ids = _employee_1_organization_ids(dataset)
    assert len(organization_ids) > 1, "Precondition: employee_1 must have more than one seeded organization"

    stale_organization_id = organization_ids[0]

    with allure.step(f"Lock {_USERNAME} in all {len(organization_ids)} seeded organizations"):
        for organization_id in organization_ids:
            lock_membership(user_id=user_id, organization_id=organization_id)

    with allure.step("POST /connect/token with the stale organization_id — expect success, not user_is_locked_in_organization"):
        response = requests.post(
            f"{global_settings.backend_base_url}/connect/token",
            data={
                "grant_type": "password",
                "scope": "offline_access",
                "username": _USERNAME,
                "storeId": global_settings.store_id,
                "password": global_settings.users_password.get_secret_value(),
                "organization_id": stale_organization_id,
            },
            timeout=global_settings.requests_timeout,
            verify=global_settings.verify_ssl,
        )

    with allure.step("Verify sign-in succeeded"):
        assert response.status_code == 200, (
            f"Expected sign-in to succeed once the stale organization_id is dropped, "
            f"got {response.status_code}: {response.text}"
        )
        assert "access_token" in response.json()
