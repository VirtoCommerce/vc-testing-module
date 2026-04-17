"""API key CRUD — migrated from Katalon `API Coverage/ModulePlatform/ApiKey*`.

The POST /api/platform/security/users/apikeys endpoint returns 200 with an
empty body (no JSON). To find the newly created key, we diff the GET results
before and after creation.
"""

import uuid

import allure
import pytest

from restapi.operations import ApiKeyOperations, UserOperations


def _create_key_and_find(api_key_ops: ApiKeyOperations, user_id: str, key_name: str) -> dict:
    """Create an API key and return it by diffing before/after GET."""
    before_ids = {k["id"] for k in (api_key_ops.get_by_user_id(user_id) or [])}
    api_key_ops.create(user_id=user_id, name=key_name)
    after = api_key_ops.get_by_user_id(user_id) or []
    new_keys = [k for k in after if k["id"] not in before_ids]
    assert len(new_keys) == 1, f"Expected 1 new key, got {len(new_keys)}"
    return new_keys[0]


@pytest.mark.restapi
@allure.feature("Platform / API Keys (REST API)")
@allure.title("Create API key for user")
def test_api_key_create(make_user, user_ops: UserOperations, api_key_ops: ApiKeyOperations) -> None:
    user = make_user()
    full_user = user_ops.get_by_name(user["user_name"])

    with allure.step("POST /api/platform/security/users/apikeys"):
        key = _create_key_and_find(api_key_ops, full_user["id"], f"QAKey_{uuid.uuid4().hex[:8]}")

    with allure.step("Verify API key created"):
        assert key["id"]
        assert key["isActive"] is True

    with allure.step("Cleanup"):
        api_key_ops.delete([key["id"]])


@pytest.mark.restapi
@allure.feature("Platform / API Keys (REST API)")
@allure.title("Get API keys by user id")
def test_api_key_get_by_user(make_user, user_ops: UserOperations, api_key_ops: ApiKeyOperations) -> None:
    user = make_user()
    full_user = user_ops.get_by_name(user["user_name"])
    key = _create_key_and_find(api_key_ops, full_user["id"], f"QAKey_{uuid.uuid4().hex[:8]}")

    with allure.step(f"GET /api/platform/security/users/{full_user['id']}/apikeys"):
        keys = api_key_ops.get_by_user_id(full_user["id"])

    with allure.step("Verify key found"):
        assert isinstance(keys, list)
        assert any(k["id"] == key["id"] for k in keys)

    with allure.step("Cleanup"):
        api_key_ops.delete([key["id"]])


@pytest.mark.restapi
@allure.feature("Platform / API Keys (REST API)")
@allure.title("Update API key — deactivate")
def test_api_key_update(make_user, user_ops: UserOperations, api_key_ops: ApiKeyOperations) -> None:
    user = make_user()
    full_user = user_ops.get_by_name(user["user_name"])
    key = _create_key_and_find(api_key_ops, full_user["id"], f"QAKey_{uuid.uuid4().hex[:8]}")

    with allure.step("PUT /api/platform/security/users/apikeys — isActive=false"):
        api_key_ops.update(key, isActive=False)

    with allure.step("Verify deactivated"):
        keys = api_key_ops.get_by_user_id(full_user["id"])
        updated = next((k for k in keys if k["id"] == key["id"]), None)
        assert updated is not None
        assert updated["isActive"] is False

    with allure.step("Cleanup"):
        api_key_ops.delete([key["id"]])


@pytest.mark.restapi
@allure.feature("Platform / API Keys (REST API)")
@allure.title("Delete API key")
def test_api_key_delete(make_user, user_ops: UserOperations, api_key_ops: ApiKeyOperations) -> None:
    user = make_user()
    full_user = user_ops.get_by_name(user["user_name"])
    key = _create_key_and_find(api_key_ops, full_user["id"], f"QAKey_{uuid.uuid4().hex[:8]}")

    with allure.step(f"DELETE /api/platform/security/users/apikeys ids=[{key['id']}]"):
        api_key_ops.delete([key["id"]])

    with allure.step("Verify key removed"):
        keys = api_key_ops.get_by_user_id(full_user["id"])
        assert not any(k["id"] == key["id"] for k in keys)
