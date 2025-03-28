import allure
import os
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_user import TEST_ADMIN_USER


@allure.title("Get anonymous user (GraphQL)")
def test_get_anonymous_user(auth_token, graphql_client):
    print(f"{os.linesep}Running test to get anonymous user...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user_response = user_operations.get_me()

    assert user_response["me"]["id"] is not None, "User ID is None"
    assert user_response["me"]["userName"] == "Anonymous", "User name is not Anonymous"


@allure.title("Get current registered user (GraphQL)")
def test_get_current_registered_user(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to get current registered user...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user_response = user_operations.get_me(auth_required=True)

    assert user_response["me"]["id"] is not None, "User ID is None"
    assert user_response["me"]["userName"] == config["username"], "User name is not correct"


@allure.title("Get registered user by id (GraphQL)")
def test_get_registered_user_by_id(auth_token, graphql_client):
    print(f"{os.linesep}Running test to get registered user by id...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user_response = user_operations.get_me(TEST_ADMIN_USER["id"], auth_required=True)

    print(user_response["me"]["userName"])

    assert user_response["me"]["id"] is not None, "User ID is None"
    assert user_response["me"]["userName"] == TEST_ADMIN_USER["username"], "User name is not correct"
