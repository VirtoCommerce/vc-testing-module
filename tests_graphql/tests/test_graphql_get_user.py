import allure, os, pytest
from graphql_operations.user.user_operations import UserOperations
from test_data.test_user import TEST_ADMIN_USER
from fixtures.graphql_client_fixture import GraphQLClient
from fixtures.auth_fixture import Auth


@pytest.mark.graphql
@allure.title("Get current anonymous user (GraphQL)")
def test_get_current_anonymous_user(graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to get current anonymous user...", end=" ")

    user_operations = UserOperations(graphql_client)

    user = user_operations.get_user()

    assert user["id"] is not None, "User ID is None"
    assert user["userName"] == "Anonymous", "User name is not Anonymous"


@pytest.mark.graphql
@allure.title("Get current registered user (GraphQL)")
def test_get_current_registered_user(auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to get current registered user...", end=" ")

    user_operations = UserOperations(graphql_client)

    auth.authenticate(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

    user = user_operations.get_user()

    auth.clear_token()

    assert user["id"] is not None, "User ID is None"
    assert user["userName"] == TEST_ADMIN_USER["username"], "User name is not correct"


@pytest.mark.graphql
@allure.title("Get registered user by id (GraphQL)")
def test_get_registered_user_by_id(auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to get registered user by id...", end=" ")

    user_operations = UserOperations(graphql_client)

    auth.authenticate(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

    user = user_operations.get_user(TEST_ADMIN_USER["id"])

    auth.clear_token()

    assert user["id"] is not None, "User ID is None"
    assert user["userName"] == TEST_ADMIN_USER["username"], "User name is not correct"
