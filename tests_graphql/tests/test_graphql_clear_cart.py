import os
from typing import Any

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Clear anonymous cart (GraphQL)")
def test_clear_anonymous_cart(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to clear anonymous cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    product_id_in_stock = next(
        product_inventory
        for product_inventory in dataset["productsInventories"]
        if product_inventory["inStockQuantity"] > 0
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

    updated_cart = cart_operations.clear_cart(
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
            "cartId": updated_cart["id"],
            "userId": user["id"],
        }
    )

    assert updated_cart["id"] is not None, "Cart ID is None"
    assert updated_cart["id"] == cart["id"], "Cart ID is not the same"
    assert updated_cart["customerId"] == user["id"], "Customer ID is not the same"
    assert updated_cart["itemsQuantity"] == 0, "Items quantity is not 0"
