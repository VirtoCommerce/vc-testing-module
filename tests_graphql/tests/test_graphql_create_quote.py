import os

import allure
import pytest

from fixtures import Auth, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.quote.quote_operations import QuoteOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_PRODUCT_1
from test_data.test_user import TEST_ADMIN_USER


@pytest.mark.graphql
@allure.title("Create empty quote (GraphQL)")
def test_create_empty_quote(config: dict, auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to create empty quote...", end=" ")

    user_operations = UserOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    auth.authenticate(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

    user = user_operations.get_user()

    quote = quote_operations.create_quote(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
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
    config: dict, auth: Auth, graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to create quote with items from cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    auth.authenticate(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

    user = user_operations.get_user()

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
        quote["items"][0]["productId"] == TEST_PRODUCT_1["id"]
    ), "Quote item product ID is not correct"
