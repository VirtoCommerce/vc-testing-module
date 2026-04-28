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
@allure.title("Get shipment costs (GraphQL)")
def test_get_shipment_costs(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to get shipment costs...", end=" ")

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

    dataset_user = dataset["users"][1]

    auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"])

    user = user_operations.get_me()

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

    bopis_shipping_method = next(
        (
            shipping_method
            for shipping_method in cart["availableShippingMethods"]
            if shipping_method["code"] == "BuyOnlinePickupInStore"
        )
    )
    fixed_rate_ground_shipping_method = next(
        (
            shipping_method
            for shipping_method in cart["availableShippingMethods"]
            if shipping_method["code"] == "FixedRate"
            and shipping_method["optionName"] == "Ground"
        )
    )
    fixed_rate_air_shipping_method = next(
        (
            shipping_method
            for shipping_method in cart["availableShippingMethods"]
            if shipping_method["code"] == "FixedRate"
            and shipping_method["optionName"] == "Air"
        )
    )

    cart = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "shipment": {
                "shipmentMethodCode": fixed_rate_ground_shipping_method["code"],
                "shipmentMethodOption": fixed_rate_ground_shipping_method["optionName"],
                "price": fixed_rate_ground_shipping_method["price"]["amount"],
            },
        }
    )

    manual_payment_method = next(
        (
            paymentMethod
            for paymentMethod in cart["availablePaymentMethods"]
            if paymentMethod["code"] == "DefaultManualPaymentMethod"
        )
    )
    payment = {
        "paymentGatewayCode": manual_payment_method["code"],
        "price": manual_payment_method["price"]["amount"],
    }

    cart = cart_operations.add_or_update_cart_payment(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "payment": payment,
        }
    )

    cart_operations.create_order_from_cart(
        payload={
            "cartId": cart["id"],
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

    cart = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "shipment": {
                "shipmentMethodCode": fixed_rate_ground_shipping_method["code"],
                "shipmentMethodOption": fixed_rate_ground_shipping_method["optionName"],
                "price": fixed_rate_ground_shipping_method["price"]["amount"],
            },
        }
    )

    shipment_id = cart["shipments"][0]["id"]

    cart = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "shipment": {
                "id": shipment_id,
                "shipmentMethodCode": fixed_rate_air_shipping_method["code"],
                "shipmentMethodOption": fixed_rate_air_shipping_method["optionName"],
                "price": fixed_rate_air_shipping_method["price"]["amount"],
            },
        }
    )

    cart = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "shipment": {
                "id": shipment_id,
                "shipmentMethodCode": bopis_shipping_method["code"],
                "shipmentMethodOption": bopis_shipping_method["optionName"],
                "price": bopis_shipping_method["price"]["amount"],
            },
        }
    )

    # Test teardown

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    assert cart["shipments"] is not None, "Shipments are None"
    assert len(cart["shipments"]) == 1, "Cart has not 1 shipment"
    assert (
        cart["shipments"][0]["shipmentMethodCode"] == bopis_shipping_method["code"]
    ), "Shipment method code is not the same"
    assert (
        cart["shipments"][0]["shipmentMethodOption"]
        == bopis_shipping_method["optionName"]
    ), "Shipment method option is not the same"
    assert (
        cart["shippingTotal"]["amount"] == bopis_shipping_method["price"]["amount"]
    ), "Shipping total is not the same"
