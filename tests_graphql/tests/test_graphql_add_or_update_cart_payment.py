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
@allure.title("Add cart payment (GraphQL)")
def test_add_cart_payment(config: Dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to add a cart payment...", end=" ")

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
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "payment": payment,
        }
    )

    cart_payment = cart_with_payment["payments"][0]

    # Test teardown
    cart_operations.clear_payments(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
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
def test_update_cart_payment(config: Dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to update a cart payment...", end=" ")

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
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
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
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "payment": new_payment,
        }
    )

    updated_payment = updated_cart["payments"][0]

    # Test teardown
    cart_operations.clear_payments(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
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
