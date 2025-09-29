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
@allure.title("Update shopping list (GraphQL)")
def test_update_shopping_list(
    config: dict[str, Any],
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to update shopping list...", end=" ")

    user_operations = UserOperations(graphql_client)
    shopping_lists_operations = ShoppingListsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    dataset_user = dataset["users"][0]

    auth.authenticate(
        dataset_user["userName"],
        config["users_password"],
    )

    user = user_operations.get_me()

    new_shopping_list = shopping_lists_operations.create_shopping_list(
        payload={
            "userId": user["id"],
            "storeId": config["store_id"],
            "listName": "Test shopping list",
            "cultureName": culture,
            "currencyCode": currency,
            "scope": "Organization",
        }
    )

    updated_shopping_list = shopping_lists_operations.update_shopping_list(
        payload={
            "listId": new_shopping_list["id"],
            "listName": "Updated shopping list",
            "description": "Updated description",
            "cultureName": culture,
            "scope": "Private",
        }
    )

    # Test teardown
    shopping_lists_operations.remove_shopping_list(
        payload={
            "listId": new_shopping_list["id"],
        }
    )

    auth.clear_token()

    assert updated_shopping_list["id"] is not None, "Shopping list ID is not set"
    assert (
        updated_shopping_list["id"] == new_shopping_list["id"]
    ), "Shopping list ID does not match"
    assert (
        updated_shopping_list["name"] == "Updated shopping list"
    ), "Shopping list name does not match"
    assert (
        updated_shopping_list["scope"] == "Private"
    ), "Shopping list scope does not match"
