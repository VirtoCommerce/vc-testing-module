import os
import random
from typing import Any, Dict

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Add items to anonymous cart (GraphQL)")
def test_add_items_to_anonymous_cart(
    config: Dict[str, Any], dataset: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to add items to anonymous cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    product_id_in_stock_1 = random.choice(
        [
            product_inventory
            for product_inventory in dataset["productsInventories"]
            if product_inventory["inStockQuantity"] > 0
        ]
    )["productId"]
    product_id_in_stock_2 = random.choice(
        [
            product_inventory
            for product_inventory in dataset["productsInventories"]
            if product_inventory["inStockQuantity"] > 0
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
                    "quantity": 5,
                },
                {
                    "productId": product_id_in_stock_2,
                    "quantity": 10,
                },
            ],
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    assert cart["id"] is not None, "Cart ID is None"
    assert cart["customerId"] == user["id"], "Customer ID is not the same"
    assert cart["itemsQuantity"] == 15, "Items quantity is not the same"
