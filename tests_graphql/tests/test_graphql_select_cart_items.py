import os
import random
from typing import Any

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Select cart items (GraphQL)")
def test_select_cart_items(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to select cart items...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    product_id_in_stock_1 = random.choice(
        [
            product
            for product in dataset["productInventories"]
            if product["inStockQuantity"] > 0
        ]
    )["productId"]
    product_id_in_stock_2 = random.choice(
        [
            product
            for product in dataset["productInventories"]
            if product["inStockQuantity"] > 0
        ]
    )["productId"]

    user = user_operations.get_me()

    cart_operations.add_items_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "cartItems": [
                {
                    "productId": product_id_in_stock_1,
                    "quantity": 1,
                },
                {
                    "productId": product_id_in_stock_2,
                    "quantity": 2,
                },
            ],
        }
    )

    cart = cart_operations.unselect_all_cart_items(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    line_item_to_select = next(
        item for item in cart["items"] if item["productId"] == product_id_in_stock_2
    )

    updated_cart = cart_operations.select_cart_items(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "lineItemIds": [line_item_to_select["id"]],
        }
    )

    selected_line_item = next(
        item
        for item in updated_cart["items"]
        if item["productId"] == product_id_in_stock_2
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
    assert updated_cart["itemsQuantity"] == sum(
        item["quantity"] for item in updated_cart["items"]
    ), "Updated cart items quantity mismatch"
    assert (
        selected_line_item["selectedForCheckout"] is True
    ), "Selected line item is not selected for checkout"
    assert (
        selected_line_item["productId"] == product_id_in_stock_2
    ), "Selected line item product ID mismatch"
    assert selected_line_item["quantity"] == 2, "Selected line item quantity mismatch"


@pytest.mark.graphql
@allure.title("Select all cart items (GraphQL)")
def test_select_all_cart_items(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to select all cart items...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    product_id_in_stock_1 = random.choice(
        [
            product
            for product in dataset["productInventories"]
            if product["inStockQuantity"] > 0
        ]
    )["productId"]
    product_id_in_stock_2 = random.choice(
        [
            product
            for product in dataset["productInventories"]
            if product["inStockQuantity"] > 0
        ]
    )["productId"]

    user = user_operations.get_me()

    cart_operations.add_items_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "cartItems": [
                {
                    "productId": product_id_in_stock_1,
                    "quantity": 1,
                },
                {
                    "productId": product_id_in_stock_2,
                    "quantity": 2,
                },
            ],
        }
    )

    cart_operations.unselect_all_cart_items(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    cart = cart_operations.select_all_cart_items(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    assert cart["id"] is not None, "Cart ID is missing"
    assert cart["customerId"] == user["id"], "Cart customer ID mismatch"
    assert cart["itemsQuantity"] == sum(
        item["quantity"] for item in cart["items"]
    ), "Cart items quantity mismatch"
    assert all(
        item["selectedForCheckout"] for item in cart["items"]
    ), "All cart items are not selected for checkout"
