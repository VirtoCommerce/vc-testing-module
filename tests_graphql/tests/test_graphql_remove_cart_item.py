import os
from typing import Any

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Remove item from cart (GraphQL)")
def test_remove_item_from_cart(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to remove item from cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    product_id_in_stock = next(
        product_inventory
        for product_inventory in dataset["productInventories"]
        if product_inventory["inStockQuantity"] > 0
    )["productId"]

    user = user_operations.get_me()

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "productId": product_id_in_stock,
            "quantity": 1,
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    line_item = cart["items"][0]

    updated_cart = cart_operations.remove_cart_item(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "lineItemId": line_item["id"],
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": updated_cart["id"],
            "userId": user["id"],
        }
    )

    assert updated_cart["id"] is not None, "Updated cart ID is missing"
    assert updated_cart["id"] == cart["id"], "Updated cart ID mismatch"
    assert updated_cart["customerId"] == user["id"], "Updated cart customer ID mismatch"
    assert updated_cart["itemsQuantity"] == 0, "Updated cart items quantity mismatch"
