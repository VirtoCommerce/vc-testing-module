import os
import random
from typing import Any, Dict

import allure
import pytest

from fixtures.graphql_client_fixture import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Unselect cart items (GraphQL)")
def test_unselect_cart_items(
    config: Dict[str, Any], dataset: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to unselect cart items...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    product_id_in_stock_1 = random.choice(
        [
            product
            for product in dataset["productsInventories"]
            if product["inStockQuantity"] > "0"
        ]
    )["productId"]
    product_id_in_stock_2 = random.choice(
        [
            product
            for product in dataset["productsInventories"]
            if product["inStockQuantity"] > "0"
        ]
    )["productId"]

    user = user_operations.get_me()

    cart = cart_operations.add_items_to_cart(
        payload={
            "storeId": config["store_id"],
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

    line_item_to_unselect = next(
        item for item in cart["items"] if item["productId"] == product_id_in_stock_2
    )

    updated_cart = cart_operations.unselect_cart_items(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "lineItemIds": [line_item_to_unselect["id"]],
        }
    )

    unselected_line_item = next(
        item
        for item in updated_cart["items"]
        if item["productId"] == product_id_in_stock_2
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    assert updated_cart["id"] is not None
    assert updated_cart["id"] == cart["id"]
    assert updated_cart["customerId"] == user["id"]
    assert updated_cart["itemsQuantity"] == sum(
        item["quantity"] for item in updated_cart["items"]
    )
    assert unselected_line_item["selectedForCheckout"] is False
    assert unselected_line_item["productId"] == product_id_in_stock_2
    assert unselected_line_item["quantity"] == 2


@pytest.mark.graphql
@allure.title("Unselect all cart items (GraphQL)")
def test_unselect_all_cart_items(
    config: Dict[str, Any], dataset: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to unselect all cart items...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    product_id_in_stock_1 = random.choice(
        [
            product
            for product in dataset["productsInventories"]
            if product["inStockQuantity"] > "0"
        ]
    )["productId"]
    product_id_in_stock_2 = random.choice(
        [
            product
            for product in dataset["productsInventories"]
            if product["inStockQuantity"] > "0"
        ]
    )["productId"]

    user = user_operations.get_me()

    cart_operations.add_items_to_cart(
        payload={
            "storeId": config["store_id"],
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
            "storeId": config["store_id"],
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

    assert cart["id"] is not None
    assert cart["customerId"] == user["id"]
    assert cart["itemsQuantity"] == sum(item["quantity"] for item in cart["items"])
    assert all(item["selectedForCheckout"] for item in cart["items"]) is False
