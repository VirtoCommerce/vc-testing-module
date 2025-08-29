import os
from typing import Any, Dict

import allure
import pytest

from fixtures import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_PRODUCT_1


@pytest.mark.graphql
@allure.title("Add item to anonymous cart (GraphQL)")
def test_add_item_to_anonymous_cart(
    config: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to add item to anonymous cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    user = user_operations.get_user()

    cart_operations = CartOperations(graphql_client)
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "productId": TEST_PRODUCT_1["id"],
            "quantity": 1,
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
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
