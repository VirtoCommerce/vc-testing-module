import os

import allure
import pytest

from fixtures.graphql_client_fixture import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_PRODUCT_1, TEST_PRODUCT_2


@pytest.mark.graphql
@allure.title("Unselect cart items (GraphQL)")
def test_unselect_cart_items(config: dict, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to unselect cart items...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    cart = cart_operations.add_items_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "cartItems": [
                {
                    "productId": TEST_PRODUCT_1["id"],
                    "quantity": 1,
                },
                {
                    "productId": TEST_PRODUCT_2["id"],
                    "quantity": 2,
                },
            ],
        }
    )

    line_item_to_unselect = next(
        item for item in cart["items"] if item["productId"] == TEST_PRODUCT_2["id"]
    )

    updated_cart = cart_operations.unselect_cart_items(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "lineItemIds": [line_item_to_unselect["id"]],
        }
    )

    unselected_line_item = next(
        item
        for item in updated_cart["items"]
        if item["productId"] == TEST_PRODUCT_2["id"]
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    assert updated_cart["id"] is not None
    assert updated_cart["id"] == cart["id"]
    assert updated_cart["customerId"] == user["id"]
    assert updated_cart["itemsQuantity"] == sum(
        item["quantity"] for item in updated_cart["items"]
    )
    assert unselected_line_item["selectedForCheckout"] is False
    assert unselected_line_item["productId"] == TEST_PRODUCT_2["id"]
    assert unselected_line_item["quantity"] == 2


@pytest.mark.graphql
@allure.title("Unselect all cart items (GraphQL)")
def test_unselect_all_cart_items(config: dict, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to unselect all cart items...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    cart_operations.add_items_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "cartItems": [
                {
                    "productId": TEST_PRODUCT_1["id"],
                    "quantity": 1,
                },
                {
                    "productId": TEST_PRODUCT_2["id"],
                    "quantity": 2,
                },
            ],
        }
    )

    cart = cart_operations.unselect_all_cart_items(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
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

    assert cart["id"] is not None
    assert cart["customerId"] == user["id"]
    assert cart["itemsQuantity"] == sum(item["quantity"] for item in cart["items"])
    assert all(item["selectedForCheckout"] for item in cart["items"]) is False
