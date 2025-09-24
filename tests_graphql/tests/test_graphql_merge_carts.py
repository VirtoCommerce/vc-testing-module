import os
import random
from typing import Any, Dict

import allure
import pytest

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Merge carts (GraphQL)")
def test_merge_carts(
    config: Dict[str, Any],
    dataset: Dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to merge carts...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    dataset_user = dataset["users"][0]
    product_id_in_stock = random.choice(
        [
            product_inventory
            for product_inventory in dataset["productsInventories"]
            if product_inventory["inStockQuantity"] > "0"
        ]
    )["productId"]

    anonymous_user = user_operations.get_me()

    anonymous_cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": anonymous_user["id"],
            "productId": product_id_in_stock,
            "quantity": 1,
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    auth.authenticate(dataset_user["userName"], config["users_password"])

    registered_user = user_operations.get_me()

    registered_user_cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": registered_user["id"],
            "productId": product_id_in_stock,
            "quantity": 2,
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    merged_cart = cart_operations.merge_cart(
        payload={
            "storeId": config["store_id"],
            "userId": registered_user["id"],
            "secondCartId": anonymous_cart["id"],
            "cultureName": culture,
            "currencyCode": currency,
            "deleteAfterMerge": True,
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": merged_cart["id"],
            "userId": registered_user["id"],
        }
    )

    auth.clear_token()

    assert merged_cart["id"] is not None, "Merged cart ID is missing"
    assert merged_cart["id"] == registered_user_cart["id"], "Merged cart ID mismatch"
    assert merged_cart["itemsQuantity"] == 3, "Merged cart items quantity mismatch"
