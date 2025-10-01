import os
import random
from typing import Any

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Apply cart coupon (GraphQL)")
def test_add_cart_coupon(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to apply coupon to cart...", end=" ")

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    coupon_code = dataset["coupons"][0]["code"]
    product_id_in_stock = random.choice(
        [
            product_inventory
            for product_inventory in dataset["productInventories"]
            if product_inventory["inStockQuantity"] > 0
        ]
    )["productId"]

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_me()

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "productId": product_id_in_stock,
            "quantity": 1,
        }
    )

    cart_with_coupon = cart_operations.apply_coupon(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "couponCode": coupon_code,
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    applied_coupon = cart_with_coupon["coupons"][0]

    # Test teardown
    cart_operations.remove_coupon(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "couponCode": coupon_code,
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    cart_operations.remove_cart(
        payload={
            "cartId": cart_with_coupon["id"],
            "userId": user["id"],
        }
    )

    assert cart_with_coupon["id"] == cart["id"], "Cart ID is not the same"
    assert applied_coupon["isAppliedSuccessfully"], "Coupon is not applied successfully"
    assert applied_coupon["code"] == coupon_code, "Coupon code is not the same"
    assert (
        cart_with_coupon["discountTotal"]["amount"] > 0
    ), "Discount total is not greater than 0"
