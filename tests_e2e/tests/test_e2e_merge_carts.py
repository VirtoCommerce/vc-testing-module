import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import CartPage, HomePage, SignInPage


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

    product = dataset["products"][14]
    quantity_to_add = 2

    anonymous_cart = None
    anonymous_user_id = None

    try:
        # Step 1: Add item to cart as anonymous user
        home_page = HomePage(page, config)
        home_page.navigate()

        anonymous_user_id = page.evaluate("() => localStorage.getItem('user-id')")

        anonymous_cart = cart_operations.add_item_to_cart(
            payload={
                "storeId": config["STORE_ID"],
                "userId": anonymous_user_id,
                "productId": product["code"],
                "quantity": quantity_to_add,
            }
        )

        page.reload()

        expect(
            home_page.cart_items_badge, "Cart items badge is not visible"
        ).to_be_visible()

        # Step 2: Sign in as registered user (triggers cart merge)
        sign_in_page = SignInPage(page, config)
        sign_in_page.navigate()
        sign_in_page.sign_in(dataset["users"][0]["userName"], config["USERS_PASSWORD"])

        # Step 3: Navigate to cart and verify anonymous cart was merged
        cart_page = CartPage(config, page)
        cart_page.navigate()

        assert not cart_page.is_empty, "Cart is empty after sign in - anonymous cart was not merged"

        line_item = cart_page.get_line_item_by_sku(product["code"])

        assert line_item is not None, (
            f"Product {product['code']} not found in cart after merge"
        )
        assert line_item.sku == product["code"], (
            f"Line item SKU mismatch: expected {product['code']}, got {line_item.sku}"
        )
        assert str(line_item.quantity_stepper_component.quantity_input.input_value()) == str(
            quantity_to_add
        ), f"Line item quantity mismatch: expected {quantity_to_add}"

    finally:
        # Teardown: Remove anonymous cart and registered user's cart
        registered_user = None
        registered_user_cart = None

        try:
            auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"])
            registered_user = user_operations.get_me()
            registered_user_cart = cart_operations.get_cart(
                store_id=config["STORE_ID"],
                user_id=registered_user["id"],
                currency_code="USD",
                culture_name="en-US",
            )
            auth.clear_token()
        except Exception:
            pass

        auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])

        if anonymous_cart and anonymous_user_id:
            try:
                cart_operations.remove_cart(
                    payload={
                        "cartId": anonymous_cart["id"],
                        "userId": anonymous_user_id,
                    }
                )
            except Exception:
                pass  # Anonymous cart may already be consumed by merge

        if registered_user_cart and registered_user:
            try:
                cart_operations.remove_cart(
                    payload={
                        "cartId": registered_user_cart["id"],
                        "userId": registered_user["id"],
                    }
                )
            except Exception:
                pass

        auth.clear_token()
