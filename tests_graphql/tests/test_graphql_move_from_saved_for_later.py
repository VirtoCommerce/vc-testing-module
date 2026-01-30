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
@allure.title("Move from saved for later (GraphQL)")
def test_graphql_move_from_saved_for_later(
    config: Config,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
    auth: Auth,
):
    print(f"{os.linesep}Running test to move from saved for later...", end=" ")

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

    # Add item to cart
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

    # Move item to saved for later
    saved_for_later_operations.move_to_saved_for_later(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "cartId": cart["id"],
            "lineItemIds": [line_item_id],
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    # Get saved for later list to get the line item id
    saved_for_later = saved_for_later_operations.get_saved_for_later(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
    )

    saved_line_item_id = saved_for_later["items"][0]["id"]

    # Move item from saved for later back to cart
    move_result = saved_for_later_operations.move_from_saved_for_later(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "cartId": cart["id"],
            "lineItemIds": [saved_line_item_id],
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    # Test teardown
    if saved_for_later and saved_for_later["items"]:
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
    assert move_result is not None, "Move from saved for later result is None"
    assert move_result["cart"] is not None, "Cart in move result is None"
    assert move_result["list"] is not None, "List in move result is None"

    # Verify item was added back to cart
    assert move_result["cart"]["itemsQuantity"] == 1, "Item should be added back to cart"

    # Verify item is removed from saved for later list
    assert move_result["list"]["itemsQuantity"] == 0, "Saved for later list should be empty"

    # Verify the correct product is in cart
    cart_items = move_result["cart"]["items"]
    assert len(cart_items) == 1, "Should have exactly 1 item in cart"
    assert cart_items[0]["productId"] == product_id, "Cart item product ID mismatch"
