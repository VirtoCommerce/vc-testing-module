import os
import random
from typing import Any

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Add cart shipment (GraphQL)")
def test_add_cart_shipment(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to add a cart shipment...", end=" ")

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
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product_id_in_stock,
            "quantity": 1,
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    ground_shipping_method = next(
        (
            shippingMethod
            for shippingMethod in cart["availableShippingMethods"]
            if shippingMethod["code"] == "FixedRate"
            and shippingMethod["optionName"] == "Ground"
        )
    )

    shipment = {
        "shipmentMethodCode": ground_shipping_method["code"],
        "shipmentMethodOption": ground_shipping_method["optionName"],
        "price": ground_shipping_method["price"]["amount"],
    }

    cart_with_shipment = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "shipment": shipment,
        }
    )

    updated_shipment = cart_with_shipment["shipments"][0]

    # Test teardown
    cart_operations.clear_shipments(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
        }
    )
    cart_operations.remove_cart(
        payload={
            "cartId": cart_with_shipment["id"],
            "userId": user["id"],
        }
    )

    assert cart_with_shipment["id"] is not None, "Cart ID is None"
    assert cart["id"] == cart_with_shipment["id"], "Cart ID is not the same"
    assert cart_with_shipment["shipments"] is not None, "Shipments are None"
    assert len(cart_with_shipment["shipments"]) > 0, "Cart has not shipments"
    assert updated_shipment is not None, "Shipment is None"
    assert updated_shipment["id"] is not None, "Shipment ID is None"
    assert (
        updated_shipment["shipmentMethodCode"] == ground_shipping_method["code"]
    ), "Shipment method code is not the same"
    assert (
        updated_shipment["shipmentMethodOption"] == ground_shipping_method["optionName"]
    ), "Shipment method option is not the same"
    assert (
        updated_shipment["price"]["amount"] == ground_shipping_method["price"]["amount"]
    ), "Shipment price is not the same"


@pytest.mark.graphql
@allure.title("Update cart shipment (GraphQL)")
def test_update_cart_shipment(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to update a cart shipment...", end=" ")

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
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product_id_in_stock,
            "quantity": 1,
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    ground_shipping_method = next(
        (
            shippingMethod
            for shippingMethod in cart["availableShippingMethods"]
            if shippingMethod["code"] == "FixedRate"
            and shippingMethod["optionName"] == "Ground"
        )
    )

    shipment = {
        "shipmentMethodCode": ground_shipping_method["code"],
        "shipmentMethodOption": ground_shipping_method["optionName"],
        "price": ground_shipping_method["price"]["amount"],
    }

    cart_with_shipment = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "shipment": shipment,
        }
    )

    air_shipping_method = next(
        (
            shippingMethod
            for shippingMethod in cart["availableShippingMethods"]
            if shippingMethod["code"] == "FixedRate"
            and shippingMethod["optionName"] == "Air"
        )
    )

    new_shipment = {
        "id": cart_with_shipment["shipments"][0]["id"],
        "shipmentMethodCode": air_shipping_method["code"],
        "shipmentMethodOption": air_shipping_method["optionName"],
        "price": air_shipping_method["price"]["amount"],
    }

    cart_with_updated_shipment = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "shipment": new_shipment,
        }
    )

    updated_shipment = cart_with_updated_shipment["shipments"][0]

    # Test teardown
    cart_operations.clear_shipments(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
        }
    )
    cart_operations.remove_cart(
        payload={
            "cartId": cart_with_updated_shipment["id"],
            "userId": user["id"],
        }
    )

    assert cart_with_shipment["id"] is not None, "Cart ID is None"
    assert cart["id"] == cart_with_shipment["id"], "Cart ID is not the same"
    assert cart_with_shipment["shipments"] is not None, "Shipments are None"
    assert len(cart_with_shipment["shipments"]) > 0, "Cart has not shipments"
    assert updated_shipment is not None, "Shipment is None"
    assert updated_shipment["id"] is not None, "Shipment ID is None"
    assert (
        updated_shipment["shipmentMethodCode"] == air_shipping_method["code"]
    ), "Shipment method code is not the same"
    assert (
        updated_shipment["shipmentMethodOption"] == air_shipping_method["optionName"]
    ), "Shipment method option is not the same"
    assert (
        updated_shipment["price"]["amount"] == air_shipping_method["price"]["amount"]
    ), "Shipment price is not the same"
