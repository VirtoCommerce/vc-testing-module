import os

import allure
import pytest

from fixtures import Auth, GraphQLClient
from graphql_operations.shopping_lists.shopping_lists_operations import (
    ShoppingListsOperations,
)
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_user import TEST_PERMANENT_CORPORATE_USER


@pytest.mark.graphql
@allure.title("Get shopping lists (GraphQL)")
def test_get_shopping_lists(config: dict, auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to get shopping lists...", end=" ")

    user_operations = UserOperations(graphql_client)
    shopping_lists_operations = ShoppingListsOperations(graphql_client)

    auth.authenticate(
        TEST_PERMANENT_CORPORATE_USER["username"],
        TEST_PERMANENT_CORPORATE_USER["password"],
    )

    user = user_operations.get_user()

    shopping_list = shopping_lists_operations.create_shopping_list(
        payload={
            "userId": user["id"],
            "storeId": config["store_id"],
            "listName": "[E2E test] Test shopping list",
            "cultureName": TEST_CULTURE["en-US"],
            "currencyCode": TEST_CURRENCY["USD"],
            "scope": "Private",
        }
    )

    shopping_lists_response = shopping_lists_operations.get_shopping_lists(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    # Test teardown

    shopping_lists_operations.remove_shopping_list(
        payload={
            "listId": shopping_list["id"],
        }
    )

    auth.clear_token()

    assert shopping_lists_response["totalCount"] == 1
