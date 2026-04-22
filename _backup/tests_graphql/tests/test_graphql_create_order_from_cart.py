import os
import random
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Create order from cart (GraphQL)")
def test_create_order_from_cart(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to create order from cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    dataset_user = dataset["users"][0]
    product_id_in_stock = random.choice(
        [
            product_inventory
            for product_inventory in dataset["productInventories"]
            if product_inventory["inStockQuantity"] > 0
        ]
    )["productId"]

    auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"])

    user = user_operations.get_me()

    cart_operations.clear_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product_id_in_stock,
            "quantity": 1,
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    shipping_method = next(
        shipping_method
        for shipping_method in cart["availableShippingMethods"]
        if shipping_method["code"] == "FixedRate" and shipping_method["optionName"] == "Ground"
    )

    cart = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "shipment": {
                "shipmentMethodCode": shipping_method["code"],
                "shipmentMethodOption": shipping_method["optionName"],
                "price": shipping_method["price"]["amount"],
            },
        }
    )

    payment_method = next(
        payment_method
        for payment_method in cart["availablePaymentMethods"]
        if payment_method["code"] == "DefaultManualPaymentMethod"
    )

    cart = cart_operations.add_or_update_cart_payment(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "payment": {
                "paymentGatewayCode": payment_method["code"],
                "price": payment_method["price"]["amount"],
            },
        }
    )

    order = cart_operations.create_order_from_cart(
        payload={
            "cartId": cart["id"],
        }
    )

    auth.clear_token()

    assert order["id"] is not None, "Order ID is None"
    assert order["number"] is not None, "Order number is None"
    assert order["items"] is not None, "Order items are None"
    assert len(order["items"]) == 1, "Order items length is not 1"
    assert order["items"][0]["productId"] == product_id_in_stock, "Order item product ID is not the same"
    assert order["items"][0]["quantity"] == 1, "Order item quantity is not 1"
