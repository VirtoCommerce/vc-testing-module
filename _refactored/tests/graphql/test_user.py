import pytest

from core.clients import GraphQLClient
from gql.operations import UserOperations

_USERNAME = "acme_store_employee_1@acme.com"


@pytest.mark.graphql
def test_user_current_anonymous(graphql_client: GraphQLClient) -> None:
    user_ops = UserOperations(client=graphql_client)

    user = user_ops.get_me()

    assert user is not None
    assert user.id is not None
    assert user.user_name == "Anonymous"


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
def test_user_current_registered(graphql_client: GraphQLClient) -> None:
    user_ops = UserOperations(client=graphql_client)

    user = user_ops.get_me()

    assert user is not None
    assert user.id is not None
    assert user.user_name == _USERNAME
