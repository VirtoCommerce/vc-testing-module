import os

import allure
import pytest

from fixtures.auth_fixture import Auth
from fixtures.graphql_client_fixture import GraphQLClient
from graphql_operations.shopping_lists.shopping_lists_operations import (
    ShoppingListsOperations,
)
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_user import TEST_PERMANENT_CORPORATE_USER


@pytest.mark.graphql
@allure.title("Update shopping list (GraphQL)")
def test_update_shopping_list(config, auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to update shopping list...", end=" ")

    user_operations = UserOperations(graphql_client)
    shopping_lists_operations = ShoppingListsOperations(graphql_client)

    auth.authenticate(
        TEST_PERMANENT_CORPORATE_USER["username"],
        TEST_PERMANENT_CORPORATE_USER["password"],
    )

    user = user_operations.get_user()

    new_shopping_list = shopping_lists_operations.create_shopping_list(
        payload={
            "userId": user["id"],
            "storeId": config["store_id"],
            "listName": "[E2E test] Test shopping list",
            "cultureName": TEST_CULTURE["en-US"],
            "currencyCode": TEST_CURRENCY["USD"],
            "scope": "Organization",
        }
    )

    updated_shopping_list = shopping_lists_operations.update_shopping_list(
        payload={
            "listId": new_shopping_list["id"],
            "listName": "[E2E test] Updated shopping list",
            "description": "Updated description",
            "cultureName": TEST_CULTURE["en-US"],
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
        updated_shopping_list["name"] == "[E2E test] Updated shopping list"
    ), "Shopping list name does not match"
    assert (
        updated_shopping_list["scope"] == "Private"
    ), "Shopping list scope does not match"
