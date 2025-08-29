import os
from typing import Any, Dict

import allure
import pytest

from fixtures import Auth, GraphQLClient
from graphql_operations.shopping_lists.shopping_lists_operations import (
    ShoppingListsOperations,
)
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_PRODUCT_1


@pytest.mark.graphql
@allure.title("Remove shopping list item (GraphQL)")
def test_remove_shopping_list_item(
    config: Dict[str, Any], auth: Auth, graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to remove shopping list item...", end=" ")

    user_operations = UserOperations(graphql_client)
    shopping_lists_operations = ShoppingListsOperations(graphql_client)

    auth.authenticate(
        config["test_permanent_customer_username"],
        config["test_permanent_customer_password"],
    )

    user = user_operations.get_user()

    new_shopping_list = shopping_lists_operations.create_shopping_list(
        payload={
            "userId": user["id"],
            "storeId": config["store_id"],
            "listName": "[E2E test] Test shopping list",
            "cultureName": TEST_CULTURE["en-US"],
            "currencyCode": TEST_CURRENCY["USD"],
            "scope": "Private",
        }
    )

    shopping_list_with_item = shopping_lists_operations.add_item_to_shopping_list(
        list_id=new_shopping_list["id"],
        product_id=TEST_PRODUCT_1["id"],
        quantity=1,
    )

    empty_shopping_list = shopping_lists_operations.remove_shopping_list_item(
        payload={
            "listId": shopping_list_with_item["id"],
            "lineItemId": shopping_list_with_item["items"][0]["id"],
        }
    )

    # Test teardown

    shopping_lists_operations.remove_shopping_list(
        payload={
            "listId": new_shopping_list["id"],
        }
    )

    auth.clear_token()

    assert empty_shopping_list["id"] is not None, "Shopping list ID is not set"
    assert (
        empty_shopping_list["id"] == new_shopping_list["id"]
    ), "Shopping list ID does not match"
    assert empty_shopping_list["itemsCount"] == 0, "Shopping list is not empty"
