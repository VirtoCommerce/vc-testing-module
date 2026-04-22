import os
from typing import Any

import allure
import pytest

from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Add items to anonymous cart (GraphQL)")
def test_add_items_to_anonymous_cart(config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to add items to anonymous cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    product_1_id = "product-acme-laptop-asus-zenbook-a14-ux3407"
    product_2_id = "product-acme-laptop-asus-vivobook-16-x1607qa"

    user = user_operations.get_me()

    cart = cart_operations.add_items_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "cartItems": [
                {
                    "productId": product_1_id,
                    "quantity": 5,
                },
                {
                    "productId": product_2_id,
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
