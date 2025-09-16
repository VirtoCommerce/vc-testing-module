import os
import random
from typing import Any, Dict

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Apply gifts for specified product (GraphQL)")
def test_gift_specific_product(
    config: Dict[str, Any], dataset: Dict[str, Any], graphql_client: GraphQLClient
):
    print(
        f"{os.linesep}Running test to apply gifts for specified product in cart...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    product_id_in_stock = random.choice(
        [
            product_inventory
            for product_inventory in dataset["productsInventories"]
            if product_inventory["inStockQuantity"] > "0"
        ]
    )["productId"]

    user = user_operations.get_me()

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "productId": product_id_in_stock,
            "quantity": 20,
        }
    )

    gift = cart["gifts"][0]

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "userId": user["id"],
            "cartId": cart["id"],
        }
    )

    assert gift["quantity"] > 0, "Gift quantity is not greater than 0"
