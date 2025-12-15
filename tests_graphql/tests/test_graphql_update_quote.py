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
@allure.title("Change quote item quantity (GraphQL)")
def test_change_quote_item_quantity(
    config: dict[str, Any],
    auth: Auth,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to change quote item quantity...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    auth.authenticate(
        dataset["users"][0]["userName"],
        config["USERS_PASSWORD"],
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
            "storeId": config["STORE_ID"],
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

    quote_operations.change_quote_item_quantity(
        payload={
            "quoteId": quote["id"],
            "lineItemId": quote["items"][0]["id"],
            "quantity": 2,
        }
    )

    updated_quote = quote_operations.get_quote(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        id=quote["id"],
        currency_code=currency,
        culture_name=culture,
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    auth.clear_token()

    assert updated_quote["id"] == quote["id"], "Quote ID is not the same"
    assert (
        updated_quote["items"][0]["selectedTierPrice"]["quantity"] == 2
    ), "Quote item quantity is not the same"


@pytest.mark.graphql
@allure.title("Change quote comment (GraphQL)")
def test_change_quote_comment(
    config: dict[str, Any],
    auth: Auth,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to change quote comment...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    auth.authenticate(
        dataset["users"][0]["userName"],
        config["USERS_PASSWORD"],
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
            "storeId": config["STORE_ID"],
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

    updated_quote = quote_operations.change_quote_comment(
        payload={
            "quoteId": quote["id"],
            "comment": "Updated comment",
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

    assert updated_quote["id"] == quote["id"], "Quote ID is not the same"
    assert (
        updated_quote["comment"] == "Updated comment"
    ), "Quote comment is not the same"


@pytest.mark.graphql
@allure.title("Remove quote shipping and billing addresses (GraphQL)")
def test_change_quote_shipping_and_billing_addresses(
    config: dict[str, Any],
    auth: Auth,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
):
    print(
        f"{os.linesep}Running test to change quote shipping and billing addresses...",
        end=" ",
    )

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    auth.authenticate(
        dataset["users"][0]["userName"],
        config["USERS_PASSWORD"],
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
            "storeId": config["STORE_ID"],
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

    test_address = {
        "city": "Springfield",
        "countryCode": "USA",
        "countryName": "United States of America",
        "line1": "742 Evergreen Terrace",
        "postalCode": "62704",
        "regionId": "IL",
        "regionName": "Illinois",
    }

    updated_quote = quote_operations.change_quote_addresses(
        payload={
            "quoteId": quote["id"],
            "addresses": [
                {**test_address, "addressType": 1},
                {**test_address, "addressType": 2},
            ],
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

    assert updated_quote["id"] == quote["id"], "Quote ID is not the same"
    assert len(updated_quote["addresses"]) == 2, "Number of addresses is not the same"
    assert any(
        addr["addressType"] == 1 for addr in updated_quote["addresses"]
    ), "Quote has no shipping address (type 1)"
    assert any(
        addr["addressType"] == 2 for addr in updated_quote["addresses"]
    ), "Quote has no billing address (type 2)"


@pytest.mark.graphql
@allure.title("Remove quote item (GraphQL)")
def test_remove_quote_item(
    config: dict[str, Any],
    auth: Auth,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to remove quote item...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    auth.authenticate(
        dataset["users"][0]["userName"],
        config["USERS_PASSWORD"],
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
            "storeId": config["STORE_ID"],
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

    updated_quote = quote_operations.remove_quote_item(
        payload={
            "quoteId": quote["id"],
            "lineItemId": quote["items"][0]["id"],
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

    assert updated_quote["id"] == quote["id"], "Quote ID is not the same"
    assert len(updated_quote["items"]) == 0, "Quote has items"


@pytest.mark.graphql
@allure.title("Submit quote request (GraphQL)")
def test_submit_quote_request(
    config: dict[str, Any],
    auth: Auth,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to submit quote request...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    auth.authenticate(
        dataset["users"][0]["userName"],
        config["USERS_PASSWORD"],
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
            "storeId": config["STORE_ID"],
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

    updated_quote = quote_operations.submit_quote(
        payload={
            "quoteId": quote["id"],
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

    assert updated_quote["id"] == quote["id"], "Quote ID is not the same"
    assert updated_quote["status"] == "Processing", "Quote status is not the same"
