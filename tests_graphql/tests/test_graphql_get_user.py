import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Get current anonymous user (GraphQL)")
def test_get_current_anonymous_user(graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to get current anonymous user...", end=" ")

    user_operations = UserOperations(graphql_client)

    user = user_operations.get_me()

    assert user["id"] is not None, "User ID is None"
    assert user["userName"] == "Anonymous", "User name is not Anonymous"


@pytest.mark.graphql
@allure.title("Get current registered user (GraphQL)")
def test_get_current_registered_user(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to get current registered user...", end=" ")

    user_operations = UserOperations(graphql_client)

    dataset_user = dataset["users"][0]

    auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"])

    user = user_operations.get_me()

    auth.clear_token()

    assert user["id"] is not None, "User ID is None"
    assert user["userName"] == dataset_user["userName"], "User name is not correct"


@pytest.mark.graphql
@allure.title("Get registered user by user name (GraphQL)")
def test_get_registered_user_by_user_name(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to get registered user by user name...", end=" ")

    user_operations = UserOperations(graphql_client)

    dataset_user = dataset["users"][0]

    auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"])

    user = user_operations.get_user_by_username(dataset_user["userName"])

    auth.clear_token()

    assert user["id"] is not None, "User ID is None"
    assert user["userName"] == dataset_user["userName"], "User name is not correct"
