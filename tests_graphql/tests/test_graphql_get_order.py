import os
from typing import Any, Dict

import allure
import pytest

from fixtures.auth_fixture import Auth
from fixtures.graphql_client_fixture import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.order.order_operations import OrderOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Get order details (GraphQL)")
def test_get_order(
    config: Dict[str, Any],
    dataset: Dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to get order details...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    order_operations = OrderOperations(graphql_client)

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

    created_order = cart_operations.create_order_from_cart(
        payload={
            "cartId": cart["id"],
        }
    )

    order = order_operations.get_order(created_order["id"])

    auth.clear_token()

    assert (
        order["id"] == created_order["id"]
    ), f"Order ID mismatch: {order['id']} != {created_order['id']}"
    assert order["number"] is not None, "Order number is missing"
    assert order["items"] is not None, "Order items are missing"
    assert (
        order["items"][0]["productId"] == product_id_in_stock
    ), f"Product ID mismatch: {order['items'][0]['productId']} != {product_id_in_stock}"
    assert (
        order["items"][0]["quantity"] == 1
    ), f"Quantity mismatch: {order['items'][0]['quantity']} != 1"
