import os
from typing import Any, Dict

import allure
import pytest

from fixtures.graphql_client_fixture import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_PRODUCT_2, TEST_PRODUCT_3


@pytest.mark.graphql
@allure.title("Apply gifts for specified product (GraphQL)")
def test_gift_specific_product(config: Dict[str, Any], graphql_client: GraphQLClient):
    print(
        f"{os.linesep}Running test to apply gifts for specified product in cart...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "productId": TEST_PRODUCT_3["id"],
            "quantity": 5,
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

    assert gift["productId"] == TEST_PRODUCT_2["id"], "Gift product ID is not correct"
    assert gift["quantity"] == 1, "Gift quantity is not correct"
