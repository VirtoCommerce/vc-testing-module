import os
from typing import Any, Dict

import allure
import pytest

from fixtures import Auth, GraphQLClient
from graphql_operations.user.user_operations import UserOperations


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
def test_get_current_registered_user(
    config: Dict[str, Any], auth: Auth, graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to get current registered user...", end=" ")

    user_operations = UserOperations(graphql_client)

    auth.authenticate(config["test_admin_username"], config["test_admin_password"])

    user = user_operations.get_user()

    auth.clear_token()

    assert user["id"] is not None, "User ID is None"
    assert user["userName"] == config["test_admin_username"], "User name is not correct"
