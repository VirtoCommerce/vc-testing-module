import os
from typing import Any

import allure
import pytest

from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Add item to anonymous cart (GraphQL)")
def test_add_item_to_anonymous_cart(config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to add item to anonymous cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    user = user_operations.get_me()

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    product_id = "product-acme-laptop-asus-vivobook-16-x1607qa"

    cart_operations = CartOperations(graphql_client)
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product_id,
            "quantity": 1,
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

    assert cart["id"] is not None, "Cart ID is None"
    assert cart["customerId"] == user["id"], "Customer ID is not the same"
    assert cart["itemsQuantity"] == 1, "Items quantity is not the same"
