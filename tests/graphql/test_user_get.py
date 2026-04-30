import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import UserOperations

_USERNAME = "acme_store_employee_1@acme.com"


@pytest.mark.graphql
@allure.feature("User (GraphQL)")
@allure.title("Get current user as anonymous")
def test_user_get_current_anonymous(graphql_client: GraphQLClient) -> None:
    user_ops = UserOperations(client=graphql_client)

    with allure.step("Call me() as anonymous user"):
        user = user_ops.get_me()

    with allure.step("Verify current user is 'Anonymous'"):
        assert user is not None
        assert user.id is not None
        assert user.user_name == "Anonymous"


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@allure.feature("User (GraphQL)")
@allure.title("Get current user as registered user")
def test_user_get_current_registered(graphql_client: GraphQLClient) -> None:
    user_ops = UserOperations(client=graphql_client)

    with allure.step(f"Call me() as registered user '{_USERNAME}'"):
        user = user_ops.get_me()

    with allure.step(f"Verify current user is '{_USERNAME}'"):
        assert user is not None
        assert user.id is not None
        assert user.user_name == _USERNAME
