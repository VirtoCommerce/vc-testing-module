import os
import random
from typing import Any

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Add cart payment (GraphQL)")
def test_add_cart_payment(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to add a cart payment...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    product_id_in_stock = random.choice(
        [
            product_inventory
            for product_inventory in dataset["productsInventories"]
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

    cart_with_payment = cart_operations.add_or_update_cart_payment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "payment": payment,
        }
    )

    cart_payment = cart_with_payment["payments"][0]

    # Test teardown
    cart_operations.clear_payments(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
        }
    )
    cart_operations.remove_cart(
        payload={
            "cartId": cart_with_payment["id"],
            "userId": user["id"],
        }
    )

    assert cart_with_payment["id"] is not None, "Cart ID is None"
    assert cart["id"] == cart_with_payment["id"], "Cart ID is not the same"
    assert cart_with_payment["payments"] is not None, "Payments are None"
    assert len(cart_with_payment["payments"]) > 0, "Cart has not payments"
    assert cart_payment is not None, "Payment is None"
    assert cart_payment["id"] is not None, "Payment ID is None"
    assert (
        cart_payment["paymentGatewayCode"] == manual_payment_method["code"]
    ), "Payment gateway code is not the same"
    assert (
        cart_payment["price"]["amount"] == manual_payment_method["price"]["amount"]
    ), "Payment price is not the same"


@pytest.mark.graphql
@allure.title("Update cart payment (GraphQL)")
def test_update_cart_payment(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to update a cart payment...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    product_id_in_stock = random.choice(
        [
            product_inventory
            for product_inventory in dataset["productsInventories"]
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

    cart_with_payment = cart_operations.add_or_update_cart_payment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "payment": payment,
        }
    )

    authorize_net_payment_method = next(
        (
            paymentMethod
            for paymentMethod in cart["availablePaymentMethods"]
            if paymentMethod["code"] == "AuthorizeNetPaymentMethod"
        )
    )

    new_payment = {
        "id": cart_with_payment["payments"][0]["id"],
        "paymentGatewayCode": authorize_net_payment_method["code"],
        "price": authorize_net_payment_method["price"]["amount"],
    }

    updated_cart = cart_operations.add_or_update_cart_payment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "payment": new_payment,
        }
    )

    updated_payment = updated_cart["payments"][0]

    # Test teardown
    cart_operations.clear_payments(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
        }
    )
    cart_operations.remove_cart(
        payload={
            "cartId": updated_cart["id"],
            "userId": user["id"],
        }
    )

    assert cart_with_payment["id"] is not None, "Cart ID is None"
    assert cart["id"] == cart_with_payment["id"], "Cart ID is not the same"
    assert cart_with_payment["payments"] is not None, "Payments are None"
    assert len(cart_with_payment["payments"]) > 0, "Cart has not payments"
    assert updated_payment is not None, "Payment is None"
    assert updated_payment["id"] is not None, "Payment ID is None"
    assert (
        updated_payment["paymentGatewayCode"] == authorize_net_payment_method["code"]
    ), "Payment gateway code is not the same"
    assert (
        updated_payment["price"]["amount"]
        == authorize_net_payment_method["price"]["amount"]
    ), "Payment price is not the same"
