import os
import random
from typing import Any

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Change cart item quantity (GraphQL)")
def test_cart_item_quantity(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to change cart item quantity...", end=" ")

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

    line_item = cart["items"][0]

    updated_cart = cart_operations.change_cart_item_quantity(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "lineItemId": line_item["id"],
            "quantity": 10,
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": updated_cart["id"],
            "userId": user["id"],
        }
    )

    assert updated_cart["id"] is not None, "Cart ID is None"
    assert updated_cart["customerId"] == user["id"], "Customer ID is not the same"
    assert updated_cart["itemsQuantity"] == 10, "Items quantity is not the same"
