"""Platform user CRUD — migrated from Katalon `API Coverage/ModulePlatform/User*`.

Originals:
- UserCreate                → test_user_create
- UserCreateAlreadyExisted  → test_user_create_already_existed
- UserSearchSetUserID       → test_user_search
- UserDelete                → test_user_delete

Key differences from Katalon:
- Each test creates its own user with a uuid-suffixed name; no dependency on
  `GlobalVariable.userName` being pre-populated.
- The factory fixture `make_user` tracks created names and cleans up at
  teardown even for negative tests that expect a duplicate-create failure.
- Password is per-test, matches the backend's password policy
  (len >= 8, upper + lower + digit + special).
"""

import allure
import pytest

from webapi_operations.platform.user_operations import UserOperations


@pytest.mark.webapi
@allure.feature("Platform / Users (WebAPI)")
@allure.title("Create user")
def test_user_create(make_user, user_operations: UserOperations):
    with allure.step("POST /api/platform/security/users/create"):
        result = make_user()

    assert result["succeeded"] is True, f"User creation failed: {result}"

    with allure.step("Verify user appears in search"):
        search = user_operations.search(search_phrase=result["user_name"])
        names = [u["userName"] for u in search.get("users", [])]
        assert result["user_name"] in names, f"Created user not in search: {names}"


@pytest.mark.webapi
@allure.feature("Platform / Users (WebAPI)")
@allure.title("Create user — duplicate user name should fail")
def test_user_create_already_existed(make_user, user_operations: UserOperations, config):
    # First creation must succeed.
    first = make_user()
    assert first["succeeded"] is True

    with allure.step("Attempt to create the same user again — expect succeeded=false"):
        second = user_operations.create(
            user_name=first["user_name"],
            email=first["email"],
            password=first["password"],
            store_id=config["STORE_ID"],
        )

    assert second["succeeded"] is False, f"Expected duplicate create to fail, but got succeeded=true: {second}"
    assert second.get("errors"), "Expected an errors field on the duplicate-create response"


@pytest.mark.webapi
@allure.feature("Platform / Users (WebAPI)")
@allure.title("Search user by phrase")
def test_user_search(make_user, user_operations: UserOperations):
    user = make_user()

    with allure.step(f"POST /api/platform/security/users/search searchPhrase={user['user_name']}"):
        search = user_operations.search(search_phrase=user["user_name"])

    assert search.get("totalCount", 0) >= 1, f"Expected at least 1 result: {search}"
    users = search.get("users", [])
    found = next((u for u in users if u["userName"] == user["user_name"]), None)
    assert found is not None, f"Created user not in search: {users}"
    assert found.get("emailConfirmed") is True, f"emailConfirmed not true: {found}"


@pytest.mark.webapi
@allure.feature("Platform / Users (WebAPI)")
@allure.title("Delete user")
def test_user_delete(make_user, user_operations: UserOperations):
    user = make_user()
    user_name = user["user_name"]

    with allure.step(f"DELETE /api/platform/security/users?names={user_name}"):
        delete_response = user_operations.delete(user_name)

    # Response body for this endpoint is {succeeded: true} on success.
    assert delete_response.get("succeeded") is True, f"Delete failed: {delete_response}"

    with allure.step("Verify user no longer appears in search"):
        search = user_operations.search(search_phrase=user_name)
        names = [u["userName"] for u in search.get("users", [])]
        assert user_name not in names, f"User still present after delete: {names}"
