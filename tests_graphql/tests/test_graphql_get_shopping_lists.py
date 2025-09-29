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
@allure.title("Get shopping lists (GraphQL)")
def test_get_shopping_lists(
    config: dict[str, Any],
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to get shopping lists...", end=" ")

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

    shopping_lists_response = shopping_lists_operations.get_shopping_lists(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
    )

    # Test teardown

    shopping_lists_operations.remove_shopping_list(
        payload={
            "listId": shopping_list["id"],
        }
    )

    auth.clear_token()

    assert (
        shopping_lists_response["totalCount"] > 0
    ), "Total count of shopping lists is not greater than 0"
    assert shopping_list["id"] in [
        shopping_list["id"] for shopping_list in shopping_lists_response["items"]
    ], "Shopping list is not in the list of shopping lists"
