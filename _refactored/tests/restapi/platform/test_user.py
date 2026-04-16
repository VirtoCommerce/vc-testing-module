"""Platform user CRUD — migrated from Katalon `API Coverage/ModulePlatform/User*`."""

import allure
import pytest

from core.global_settings import GlobalSettings
from restapi.operations import UserOperations


@pytest.mark.restapi
@allure.feature("Platform / Users (REST API)")
@allure.title("Create user")
def test_user_create(make_user, user_ops: UserOperations):
    with allure.step("POST /api/platform/security/users/create"):
        result = make_user()

    with allure.step("Verify succeeded"):
        assert result["succeeded"] is True, f"User creation failed: {result}"

    with allure.step("Verify user appears in search"):
        search = user_ops.search(search_phrase=result["user_name"])
        names = [u["userName"] for u in search.get("users", [])]
        assert result["user_name"] in names


@pytest.mark.restapi
@allure.feature("Platform / Users (REST API)")
@allure.title("Create user — duplicate user name should fail")
def test_user_create_already_existed(make_user, user_ops: UserOperations, global_settings: GlobalSettings):
    first = make_user()
    assert first["succeeded"] is True

    with allure.step("Attempt to create the same user again"):
        second = user_ops.create(
            user_name=first["user_name"],
            email=first["email"],
            password=first["password"],
            store_id=global_settings.store_id,
        )

    with allure.step("Verify succeeded=false"):
        assert second["succeeded"] is False
        assert second.get("errors")


@pytest.mark.restapi
@allure.feature("Platform / Users (REST API)")
@allure.title("Search user by phrase")
def test_user_search(make_user, user_ops: UserOperations):
    user = make_user()

    with allure.step(f"POST /api/platform/security/users/search searchPhrase={user['user_name']}"):
        search = user_ops.search(search_phrase=user["user_name"])

    with allure.step("Verify user found"):
        assert search.get("totalCount", 0) >= 1
        found = next((u for u in search.get("users", []) if u["userName"] == user["user_name"]), None)
        assert found is not None


@pytest.mark.restapi
@allure.feature("Platform / Users (REST API)")
@allure.title("Update user — change email")
def test_user_update(make_user, user_ops: UserOperations):
    user = make_user()

    with allure.step(f"GET /api/platform/security/users/{user['user_name']}"):
        full_user = user_ops.get_by_name(user["user_name"])

    new_email = f"updated_{user['email']}"

    with allure.step(f"PUT /api/platform/security/users — email={new_email}"):
        user_ops.update(full_user, email=new_email)

    with allure.step("Verify email updated via GET"):
        reloaded = user_ops.get_by_name(user["user_name"])
        assert reloaded["email"] == new_email


@pytest.mark.restapi
@allure.feature("Platform / Users (REST API)")
@allure.title("Delete user")
def test_user_delete(make_user, user_ops: UserOperations):
    user = make_user()

    with allure.step(f"DELETE /api/platform/security/users?names={user['user_name']}"):
        delete_response = user_ops.delete(user["user_name"])

    with allure.step("Verify succeeded"):
        assert delete_response.get("succeeded") is True

    with allure.step("Verify user no longer in search"):
        search = user_ops.search(search_phrase=user["user_name"])
        names = [u["userName"] for u in search.get("users", [])]
        assert user["user_name"] not in names
