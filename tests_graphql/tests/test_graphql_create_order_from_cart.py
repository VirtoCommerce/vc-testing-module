import os
import random
from typing import Any

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Create order from cart (GraphQL)")
def test_create_order_from_cart(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to create order from cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    product_id_in_stock = random.choice(
        [
            product_inventory
            for product_inventory in dataset["productInventories"]
            if product_inventory["inStockQuantity"] > 0
        ]
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

    order = cart_operations.create_order_from_cart(
        payload={
            "cartId": cart["id"],
        }
    )

    assert order["id"] is not None, "Order ID is None"
    assert order["number"] is not None, "Order number is None"
    assert order["items"] is not None, "Order items are None"
    assert len(order["items"]) == 1, "Order items length is not 1"
    assert (
        order["items"][0]["productId"] == product_id_in_stock
    ), "Order item product ID is not the same"
    assert order["items"][0]["quantity"] == 1, "Order item quantity is not 1"
