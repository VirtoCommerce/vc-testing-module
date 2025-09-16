import os
from typing import Any, Dict

import allure
import pytest

from fixtures.auth_fixture import Auth
from fixtures.graphql_client_fixture import GraphQLClient
from graphql_operations.shopping_lists.shopping_lists_operations import (
    ShoppingListsOperations,
)
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Update shopping list items (GraphQL)")
def test_update_shopping_list_items(
    config: Dict[str, Any],
    dataset: Dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to update shopping list items...", end=" ")

    user_operations = UserOperations(graphql_client)
    shopping_lists_operations = ShoppingListsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    dataset_user = dataset["users"][0]
    product_id_in_stock = next(
        product_inventory
        for product_inventory in dataset["productsInventories"]
        if product_inventory["inStockQuantity"] > "0"
    )["productId"]

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

    shopping_list_with_item = shopping_lists_operations.add_item_to_shopping_list(
        list_id=new_shopping_list["id"],
        product_id=product_id_in_stock,
        quantity=1,
    )

    shopping_list_item = shopping_list_with_item["items"][0]

    shopping_list_with_updated_item = (
        shopping_lists_operations.update_shopping_list_items(
            payload={
                "listId": new_shopping_list["id"],
                "items": [
                    {
                        "lineItemId": shopping_list_item["id"],
                        "quantity": 2,
                    }
                ],
            }
        )
    )

    # Test teardown

    shopping_lists_operations.remove_shopping_list(
        payload={
            "listId": new_shopping_list["id"],
        }
    )

    auth.clear_token()

    assert (
        shopping_list_with_updated_item["id"] is not None
    ), "Shopping list ID is not set"
    assert (
        shopping_list_with_updated_item["id"] == new_shopping_list["id"]
    ), "Shopping list ID does not match"
    assert (
        shopping_list_with_updated_item["items"][0]["quantity"] == 2
    ), "Shopping list item quantity does not match"
