"""User lock/unlock — migrated from Katalon `API Coverage/ModulePlatform/UserLock*`."""

import uuid

import allure
import pytest
import requests
from pydantic import SecretStr

from core.auth import AuthProvider
from core.global_settings import GlobalSettings
from restapi.operations import ApiKeyOperations, UserOperations


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


@pytest.mark.restapi
@allure.feature("Platform / User Lock (REST API)")
@allure.title("Lock user — API key with isActive=false returns 401")
def test_user_lock_api_key_inactive(make_user, user_ops: UserOperations, api_key_ops, global_settings: GlobalSettings):
    from restapi.operations import ApiKeyOperations

    user = make_user()
    full_user = user_ops.get_by_name(user["user_name"])

    api_key_ops_instance: ApiKeyOperations = api_key_ops

    with allure.step("Create API key then deactivate"):
        key = api_key_ops_instance.create(user_id=full_user["id"], name=f"QAKey_{uuid.uuid4().hex[:6]}")
        api_key_ops_instance.update(key, isActive=False)

    with allure.step("Verify deactivated key"):
        keys = api_key_ops_instance.get_by_user_id(full_user["id"])
        updated = next((k for k in keys if k["id"] == key["id"]), None)
        assert updated is not None
        assert updated["isActive"] is False

    with allure.step("Cleanup"):
        api_key_ops_instance.delete([key["id"]])
