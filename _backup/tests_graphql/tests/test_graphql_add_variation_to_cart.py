import os
from typing import Any

import allure
import pytest

from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Add variation to cart (GraphQL)")
def test_add_variation_to_cart(config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient):

    print(f"{os.linesep}Running test to add variation to cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    product_operations = ProductsOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    variation_id = "var-1-lenovo-thinkPad-x1-carbon-gen-13-aura-edition-variations"

    user = user_operations.get_me()

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": variation_id,
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
