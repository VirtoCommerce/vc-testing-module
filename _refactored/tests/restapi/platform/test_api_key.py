"""API key CRUD — migrated from Katalon `API Coverage/ModulePlatform/ApiKey*`."""

import uuid

import allure
import pytest

from restapi.operations import ApiKeyOperations, UserOperations


@pytest.mark.restapi
@allure.feature("Platform / API Keys (REST API)")
@allure.title("Create API key for user")
def test_api_key_create(make_user, user_ops: UserOperations, api_key_ops: ApiKeyOperations):
    user = make_user()
    full_user = user_ops.get_by_name(user["user_name"])

    with allure.step("POST /api/platform/security/apiaccounts"):
        key_name = f"QAKey_{uuid.uuid4().hex[:8]}"
        result = api_key_ops.create(user_id=full_user["id"], name=key_name)

    with allure.step("Verify API key created"):
        assert result["id"], "API account id missing"
        assert result.get("apiKey"), "apiKey field missing"
        assert result["isActive"] is True

    with allure.step("Cleanup"):
        api_key_ops.delete([result["id"]])


@pytest.mark.restapi
@allure.feature("Platform / API Keys (REST API)")
@allure.title("Get API keys by user id")
def test_api_key_get_by_user(make_user, user_ops: UserOperations, api_key_ops: ApiKeyOperations):
    user = make_user()
    full_user = user_ops.get_by_name(user["user_name"])
    key_name = f"QAKey_{uuid.uuid4().hex[:8]}"
    created = api_key_ops.create(user_id=full_user["id"], name=key_name)

    with allure.step(f"GET /api/platform/security/users/{full_user['id']}/apiaccounts"):
        keys = api_key_ops.get_by_user_id(full_user["id"])

    with allure.step("Verify key found"):
        assert isinstance(keys, list)
        assert any(k["id"] == created["id"] for k in keys)

    with allure.step("Cleanup"):
        api_key_ops.delete([created["id"]])


@pytest.mark.restapi
@allure.feature("Platform / API Keys (REST API)")
@allure.title("Update API key — deactivate")
def test_api_key_update(make_user, user_ops: UserOperations, api_key_ops: ApiKeyOperations):
    user = make_user()
    full_user = user_ops.get_by_name(user["user_name"])
    created = api_key_ops.create(user_id=full_user["id"], name=f"QAKey_{uuid.uuid4().hex[:8]}")

    with allure.step("PUT /api/platform/security/apiaccounts — isActive=false"):
        api_key_ops.update(created, isActive=False)

    with allure.step("Verify deactivated"):
        keys = api_key_ops.get_by_user_id(full_user["id"])
        updated = next((k for k in keys if k["id"] == created["id"]), None)
        assert updated is not None
        assert updated["isActive"] is False

    with allure.step("Cleanup"):
        api_key_ops.delete([created["id"]])


@pytest.mark.restapi
@allure.feature("Platform / API Keys (REST API)")
@allure.title("Delete API key")
def test_api_key_delete(make_user, user_ops: UserOperations, api_key_ops: ApiKeyOperations):
    user = make_user()
    full_user = user_ops.get_by_name(user["user_name"])
    created = api_key_ops.create(user_id=full_user["id"], name=f"QAKey_{uuid.uuid4().hex[:8]}")

    with allure.step(f"DELETE /api/platform/security/apiaccounts ids=[{created['id']}]"):
        api_key_ops.delete([created["id"]])

    with allure.step("Verify key removed"):
        keys = api_key_ops.get_by_user_id(full_user["id"])
        assert not any(k["id"] == created["id"] for k in keys)
