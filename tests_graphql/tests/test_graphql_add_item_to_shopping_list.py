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
@allure.title("Add item to shopping list (GraphQL)")
def test_add_item_to_shopping_list(
    config: dict[str, Any],
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to add item to shopping list...", end=" ")

    user_operations = UserOperations(graphql_client)
    shopping_lists_operations = ShoppingListsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    product = dataset["products"][0]

    auth.authenticate(dataset["users"][0]["userName"], config["users_password"])

    user = user_operations.get_me()

    shopping_list = shopping_lists_operations.create_shopping_list(
        payload={
            "userId": user["id"],
            "storeId": config["store_id"],
            "listName": "Test shopping list",
            "cultureName": culture,
            "currencyCode": currency,
            "scope": "Private",
        }
    )

    shopping_list_with_item = shopping_lists_operations.add_item_to_shopping_list(
        list_id=shopping_list["id"],
        product_id=product["id"],
        quantity=1,
    )

    # Test teardown

    shopping_lists_operations.remove_shopping_list(
        payload={
            "listId": shopping_list["id"],
        }
    )

    auth.clear_token()

    assert shopping_list_with_item["id"] is not None, "Shopping list ID is not set"
    assert (
        shopping_list_with_item["id"] == shopping_list["id"]
    ), "Shopping list ID does not match"
    assert (
        shopping_list_with_item["itemsCount"] == 1
    ), "Shopping list items count is not 1"
