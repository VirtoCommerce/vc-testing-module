import os

import allure
import pytest

from fixtures.auth_fixture import Auth
from fixtures.graphql_client_fixture import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.order.order_operations import OrderOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_PRODUCT_1
from test_data.test_user import TEST_ADMIN_USER


@pytest.mark.graphql
@allure.title("Get order details (GraphQL)")
def test_get_order(config: dict, auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to get order details...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    order_operations = OrderOperations(graphql_client)

    auth.authenticate(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

    user = user_operations.get_user()

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "productId": TEST_PRODUCT_1["id"],
            "quantity": 1,
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
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
        order["items"][0]["productId"] == TEST_PRODUCT_1["id"]
    ), f"Product ID mismatch: {order['items'][0]['productId']} != {TEST_PRODUCT_1['id']}"
    assert (
        order["items"][0]["quantity"] == 1
    ), f"Quantity mismatch: {order['items'][0]['quantity']} != 1"
