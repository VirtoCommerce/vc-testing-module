import os
from typing import Any, Dict

import allure
import pytest

from fixtures import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_PRODUCT_1, TEST_PRODUCT_2


@pytest.mark.graphql
@allure.title("Add bulk items to anonymous cart (GraphQL)")
def test_add_bulk_items_to_anonymous_cart(
    config: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to add bulk items to anonymous cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    add_bulk_items_response = cart_operations.add_bulk_items_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "cartItems": [
                {
                    "productSku": TEST_PRODUCT_1["sku"],
                    "quantity": 5,
                },
                {
                    "productSku": TEST_PRODUCT_2["sku"],
                    "quantity": 10,
                },
            ],
        }
    )

    cart = add_bulk_items_response["cart"]

    # Test teardown
    cart_operations.remove_cart(payload={"cartId": cart["id"], "userId": user["id"]})

    assert cart["id"] is not None, "Cart ID is None"
    assert cart["customerId"] == user["id"], "Customer ID is not the same"
    assert cart["itemsQuantity"] == 15, "Items quantity is not the same"
