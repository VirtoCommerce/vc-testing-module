import os
import random
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.quote.quote_operations import QuoteOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Create empty quote (GraphQL)")
def test_create_empty_quote(
    config: dict[str, Any],
    auth: Auth,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to create empty quote...", end=" ")

    user_operations = UserOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    auth.authenticate(
        dataset["users"][0]["userName"],
        config["users_password"],
    )

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]

    user = user_operations.get_me()

    quote = quote_operations.create_quote(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    auth.clear_token()

    assert quote["id"] is not None, "Quote ID is None"
    assert quote["number"] is not None, "Quote number is None"
    assert quote["status"] == "Draft", "Quote status is not Draft"
    assert quote["storeId"] == config["store_id"], "Quote store ID is not correct"
    assert quote["customerId"] == user["id"], "Quote customer ID is not correct"
    assert quote["comment"] is None, "Quote comment is not None"
    assert len(quote["items"]) == 0, "Quote items are not empty"


@pytest.mark.graphql
@allure.title("Create quote with items from cart (GraphQL)")
def test_create_quote_with_items_from_cart(
    config: dict[str, Any],
    auth: Auth,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to create quote with items from cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    auth.authenticate(
        dataset["users"][0]["userName"],
        config["users_password"],
    )

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    product_id_in_stock = random.choice(
        [
            product_inventory
            for product_inventory in dataset["productInventories"]
            if product_inventory["inStockQuantity"] > 0
        ]
    )["productId"]

    user = user_operations.get_me()

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "productId": product_id_in_stock,
            "quantity": 1,
            "currencyCode": currency,
            "cultureName": culture,
        }
    )

    quote = quote_operations.create_quote_from_cart(
        payload={
            "cartId": cart["id"],
            "comment": "Test comment",
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    auth.clear_token()

    assert quote["id"] is not None, "Quote ID is None"
    assert quote["number"] is not None, "Quote number is None"
    assert quote["status"] == "Draft", "Quote status is not Draft"
    assert quote["storeId"] == config["store_id"], "Quote store ID is not correct"
    assert quote["customerId"] == user["id"], "Quote customer ID is not correct"
    assert quote["comment"] == "Test comment", "Quote comment is not correct"
    assert len(quote["items"]) > 0, "Quote items are empty"
    assert (
        quote["items"][0]["productId"] == product_id_in_stock
    ), "Quote item product ID is not correct"
