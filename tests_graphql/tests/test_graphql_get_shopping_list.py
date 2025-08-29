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


@pytest.mark.graphql
@allure.title("Get shopping list (GraphQL)")
def test_get_shopping_list(
    config: Dict[str, Any], auth: Auth, graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to get shopping list...", end=" ")

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

    shopping_list = shopping_lists_operations.get_shopping_list(
        list_id=new_shopping_list["id"],
        culture_name=TEST_CULTURE["en-US"],
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
