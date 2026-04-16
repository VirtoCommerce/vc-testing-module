"""User lock/unlock — migrated from Katalon `API Coverage/ModulePlatform/UserLock*`."""

import allure
import pytest
import requests
from pydantic import SecretStr

from core.auth import AuthProvider
from core.global_settings import GlobalSettings
from restapi.operations import UserOperations


@pytest.mark.restapi
@allure.feature("Platform / User Lock (REST API)")
@allure.title("Lock user — login blocked, unlock restores access")
def test_user_lock_unlock(make_user, user_ops: UserOperations, global_settings: GlobalSettings):
    user = make_user()
    full_user = user_ops.get_by_name(user["user_name"])

    with allure.step(f"POST /api/platform/security/users/{full_user['id']}/lock"):
        user_ops.lock(full_user["id"])

    with allure.step("Verify login blocked (expect 400)"):
        response = requests.post(
            f"{global_settings.backend_base_url}/connect/token",
            data={
                "grant_type": "password",
                "username": user["user_name"],
                "password": user["password"],
            },
            timeout=global_settings.requests_timeout,
            verify=global_settings.verify_ssl,
        )
        assert response.status_code == 400, f"Expected 400 for locked user, got {response.status_code}"

    with allure.step(f"POST /api/platform/security/users/{full_user['id']}/unlock"):
        user_ops.unlock(full_user["id"])

    with allure.step("Verify login works after unlock"):
        provider = AuthProvider(global_settings)
        provider.sign_in(user["user_name"], SecretStr(user["password"]))
        assert provider.is_authenticated
        provider.sign_out()


@pytest.mark.restapi
@allure.feature("Platform / User Lock (REST API)")
@allure.title("Deleted user — login returns error")
def test_user_deleted_login_blocked(make_user, user_ops: UserOperations, global_settings: GlobalSettings):
    user = make_user()

    with allure.step("Delete user"):
        user_ops.delete(user["user_name"])

    with allure.step("Verify login fails for deleted user"):
        response = requests.post(
            f"{global_settings.backend_base_url}/connect/token",
            data={
                "grant_type": "password",
                "username": user["user_name"],
                "password": user["password"],
            },
            timeout=global_settings.requests_timeout,
            verify=global_settings.verify_ssl,
        )
        assert response.status_code == 400
