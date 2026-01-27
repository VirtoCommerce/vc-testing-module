import os
from typing import Any

import pytest
from playwright.sync_api import Page

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import CartPage, SignInPage


@pytest.mark.e2e
def test_e2e_merge_carts(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
):
    print(f"{os.linesep}Running E2E test to merge carts...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    product = dataset["products"][1]
    quantity_to_add = 2

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"])

    registered_user = user_operations.get_me()
    cart_operations.clear_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": registered_user["id"],
        }
    )
    auth.clear_token()

    page.goto(config["FRONTEND_BASE_URL"])
    page.wait_for_load_state("networkidle")

    anonymous_user_id = page.evaluate("() => localStorage.getItem('user-id')")

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": anonymous_user_id,
            "productId": product["code"],
            "quantity": quantity_to_add,
        }
    )

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(dataset["users"][0]["userName"], config["USERS_PASSWORD"])

    cart_page = CartPage(config, page)
    cart_page.navigate()

    line_item = cart_page.get_line_item_by_sku(product["code"])

    assert not cart_page.is_empty, "Cart is empty after sign in"
    assert line_item.sku == product["code"], f"Line item sku is not equal to product sku: {product['code']}"
    assert str(line_item.quantity_stepper_component.quantity_input.input_value()) == str(
        quantity_to_add
    ), f"Line item quantity is not equal to product quantity to add: {quantity_to_add}"

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"])

    cart_operations.clear_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": registered_user["id"],
        }
    )
