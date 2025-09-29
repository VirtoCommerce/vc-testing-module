import os
from typing import Any

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Apply discount for specific product (GraphQL)")
def test_product_specific_discount(
    config: dict[str, Any],
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
):
    print(
        f"{os.linesep}Running test to apply discount for specified product...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    discount_product = next(
        product
        for product in dataset["products"]
        if product["id"] == "product-acme-laptop-hp-omen-transcend-14"
    )

    user = user_operations.get_me()

    product = products_operations.get_product(
        store_id=config["store_id"],
        user_id=user["id"],
        culture_name=culture,
        currency_code=currency,
        id=discount_product["id"],
    )

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "productId": product["id"],
            "quantity": 1,
        }
    )

    line_item = next(
        line_item
        for line_item in cart["items"]
        if line_item["productId"] == product["id"]
    )

    # Test teardown

    cart_operations.remove_cart(
        payload={
            "userId": user["id"],
            "cartId": cart["id"],
        }
    )

    assert (
        product["price"]["discountAmount"]["amount"] > 0
    ), "Discount amount is not greater than 0"
    assert (
        product["price"]["list"]["amount"]
        - product["price"]["discountAmount"]["amount"]
        == product["price"]["actual"]["amount"]
    ), "Actual price is not correct"
    assert (
        line_item["discountTotal"]["amount"]
        == product["price"]["discountAmount"]["amount"]
    ), "Discount total is not correct"
    assert (
        line_item["listPrice"]["amount"] == product["price"]["list"]["amount"]
    ), "List price is not correct"
    assert (
        line_item["placedPrice"]["amount"] == product["price"]["actual"]["amount"]
    ), "Placed price is not correct"


@pytest.mark.graphql
@allure.title("Apply discount for cart subtotal (GraphQL)")
def test_cart_subtotal_discount(
    config: dict[str, Any],
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
):
    print(
        f"{os.linesep}Running test to apply discount for cart subtotal...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    discount_product = next(
        product
        for product in dataset["products"]
        if product["id"] == "product-acme-laptop-lenovo-legion-9i-gen-10"
    )

    user = user_operations.get_me()

    product = products_operations.get_product(
        store_id=config["store_id"],
        user_id=user["id"],
        culture_name=culture,
        currency_code=currency,
        id=discount_product["id"],
    )

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "productId": product["id"],
            "quantity": 1,
        }
    )

    line_item = next(
        line_item
        for line_item in cart["items"]
        if line_item["productId"] == product["id"]
    )

    # Test teardown

    cart_operations.remove_cart(
        payload={
            "userId": user["id"],
            "cartId": cart["id"],
        }
    )

    assert cart["discountTotal"]["amount"] > 0, "Discount amount is not greater than 0"
    assert cart["discountTotal"]["amount"] > 0, "Discount total is not greater than 0"
    assert (
        line_item["discountTotal"]["amount"] == cart["discountTotal"]["amount"]
    ), "Line item discount total is not equal to cart discount total"
