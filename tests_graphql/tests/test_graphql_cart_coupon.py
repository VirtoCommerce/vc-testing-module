import allure, os, pytest
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_coupon import TEST_COUPON_CODE
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_PRODUCT_3
from fixtures.graphql_client_fixture import GraphQLClient
from typing import Dict, Any


@pytest.mark.graphql
@allure.title("Apply cart coupon (GraphQL)")
def test_add_cart_coupon(config: Dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to apply coupon to cart...", end=" ")

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
            "quantity": 1,
        }
    )

    cart_with_coupon = cart_operations.apply_coupon(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "couponCode": TEST_COUPON_CODE,
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
        }
    )

    applied_coupon = cart_with_coupon["coupons"][0]

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart_with_coupon["id"],
            "userId": user["id"],
        }
    )

    assert cart_with_coupon["id"] == cart["id"], "Cart ID is not the same"
    assert applied_coupon["isAppliedSuccessfully"], "Coupon is not applied successfully"
    assert applied_coupon["code"] == TEST_COUPON_CODE, "Coupon code is not the same"


@pytest.mark.graphql
@allure.title("Remove cart coupon (GraphQL)")
def test_remove_cart_coupon(config: Dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to remove coupon from cart...", end=" ")

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
            "quantity": 1,
        }
    )

    cart_operations.apply_coupon(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "couponCode": TEST_COUPON_CODE,
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
        }
    )

    cart_without_coupon = cart_operations.remove_coupon(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "couponCode": TEST_COUPON_CODE,
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart_without_coupon["id"],
            "userId": user["id"],
        }
    )

    assert cart_without_coupon["id"] == cart["id"], "Cart ID is not the same"
    assert len(cart_without_coupon["coupons"]) == 0, "Coupon is not removed successfully"
