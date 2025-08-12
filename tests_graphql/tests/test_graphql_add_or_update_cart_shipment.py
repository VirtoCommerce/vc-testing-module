import os
from typing import Any, Dict

import allure
import pytest

from fixtures import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_PRODUCT_1


@pytest.mark.graphql
@allure.title("Add cart shipment (GraphQL)")
def test_add_cart_shipment(config: Dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to add a cart shipment...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

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
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "shipment": shipment,
        }
    )

    updated_shipment = cart_with_shipment["shipments"][0]

    # Test teardown
    cart_operations.clear_shipments(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
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
def test_update_cart_shipment(config: Dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to update a cart shipment...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

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
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
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
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "shipment": new_shipment,
        }
    )

    updated_shipment = cart_with_updated_shipment["shipments"][0]

    # Test teardown
    cart_operations.clear_shipments(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
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
