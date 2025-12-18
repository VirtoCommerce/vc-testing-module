import os
import random
from typing import Any

import allure
import pytest

from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Update cart quantity (GraphQL)")
def test_update_cart_quantity(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to update cart quantity...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    product_id_in_stock = random.choice(
        [
            product
            for product in dataset["productInventories"]
            if product["inStockQuantity"] > 0
        ]
    )["productId"]
    user = user_operations.get_me()

    quantity_to_add = 10

    cart = cart_operations.update_cart_quantity(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "items": [
                {
                    "productId": product_id_in_stock,
                    "quantity": quantity_to_add,
                }
            ],
        }
    )

    added_item = next(
        (item for item in cart["items"] if item["productId"] == product_id_in_stock),
        None,
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    assert cart is not None, "Cart is None"
    assert cart["id"] is not None, "Cart ID is None"
    assert cart["customerId"] == user["id"], "Customer ID is not the same"
    assert added_item is not None, "Added item is None"
    assert added_item["quantity"] == quantity_to_add, "Item quantity is not the same"
