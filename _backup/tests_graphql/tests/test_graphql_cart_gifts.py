import os
from typing import Any

import allure
import pytest

from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Apply gifts for specified product quantity (GraphQL)")
def test_gift_specific_product_quantity(config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient):
    print(
        f"{os.linesep}Running test to apply gifts for specified product quantity in cart...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    product_id = "product-acme-laptop-asus-vivobook-16-x1607qa"

    user = user_operations.get_me()

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "productId": product_id,
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
