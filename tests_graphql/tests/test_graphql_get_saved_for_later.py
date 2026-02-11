import os
from typing import Any

import allure
import pytest

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.saved_for_later.saved_for_later_operations import (
    SavedForLaterOperations,
)
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Get saved for later (GraphQL)")
def test_get_saved_for_later(
    config: Config,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
    auth: Auth,
):
    print(f"{os.linesep}Running test to get saved for later...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    saved_for_later_operations = SavedForLaterOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    product_id = dataset["products"][2]["id"]  # Use product that is in stock

    auth.authenticate(
        dataset["users"][0]["userName"],
        config["USERS_PASSWORD"],
    )

    user = user_operations.get_me()

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product_id,
            "quantity": 1,
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    line_item_id = cart["items"][0]["id"]

    move_result = saved_for_later_operations.move_to_saved_for_later(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "cartId": cart["id"],
            "lineItemIds": [line_item_id],
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    # Get saved for later list
    saved_for_later = saved_for_later_operations.get_saved_for_later(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
    )

    # Test teardown
    # Clean up saved for later items
    for item in saved_for_later["items"]:
        saved_for_later_operations.remove_saved_for_later_item(
            payload={
                "listId": saved_for_later["id"],
                "lineItemId": item["id"],
            }
        )

    # Remove cart
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    auth.clear_token()

    # Assertions
    assert move_result is not None, "Move to saved for later result is None"
    assert move_result["cart"] is not None, "Cart in move result is None"
    assert move_result["list"] is not None, "List in move result is None"

    # Verify item was removed from cart
    assert move_result["cart"]["itemsQuantity"] == 0, "Item should be removed from cart"

    # Verify item is in saved for later list
    assert move_result["list"]["itemsQuantity"] == 1, "Item should be in saved for later list"

    # Verify getSavedForLater query returns the list
    assert saved_for_later is not None, "Saved for later list is None"
    assert saved_for_later["itemsQuantity"] == 1, "Saved for later should have 1 item"

    # Verify the correct product is in saved for later
    saved_items = saved_for_later["items"]
    assert len(saved_items) == 1, "Should have exactly 1 saved item"
    assert saved_items[0]["productId"] == product_id, "Saved item product ID mismatch"
