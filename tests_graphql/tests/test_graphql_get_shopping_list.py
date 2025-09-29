import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from graphql_operations.shopping_lists.shopping_lists_operations import (
    ShoppingListsOperations,
)
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Get shopping list (GraphQL)")
def test_get_shopping_list(
    config: dict[str, Any],
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to get shopping list...", end=" ")

    user_operations = UserOperations(graphql_client)
    shopping_lists_operations = ShoppingListsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    dataset_user = dataset["users"][0]

    auth.authenticate(dataset_user["userName"], config["users_password"])

    user = user_operations.get_me()

    new_shopping_list = shopping_lists_operations.create_shopping_list(
        payload={
            "userId": user["id"],
            "storeId": config["store_id"],
            "listName": "Test shopping list",
            "cultureName": culture,
            "currencyCode": currency,
            "scope": "Private",
        }
    )

    shopping_list = shopping_lists_operations.get_shopping_list(
        list_id=new_shopping_list["id"],
        culture_name=culture,
    )

    # Test teardown

    shopping_lists_operations.remove_shopping_list(
        payload={
            "listId": shopping_list["id"],
        }
    )

    auth.clear_token()

    assert shopping_list["id"] is not None, "Shopping list ID is not set"
    assert (
        shopping_list["id"] == new_shopping_list["id"]
    ), "Shopping list ID does not match"
    assert (
        shopping_list["name"] == new_shopping_list["name"]
    ), "Shopping list name does not match"
    assert (
        shopping_list["storeId"] == config["store_id"]
    ), "Shopping list store ID does not match"
    assert (
        shopping_list["customerId"] == user["id"]
    ), "Shopping list customer ID does not match"
    assert shopping_list["scope"] == "Private", "Shopping list scope is not Private"
