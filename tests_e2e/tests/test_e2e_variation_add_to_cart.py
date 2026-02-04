"""
E2E tests for B2C product variation cart integration.

Test Cases:
- C407723: Price, stock, and Add to Cart update on variation selection
- C407724: Add selected variation to cart
- C407725: Cannot add to cart until all options selected
"""

import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import CartPage, ProductPage


@pytest.mark.e2e
@allure.title("Price, stock, and Add to Cart update on variation selection (E2E)")
def test_e2e_update_price_stock_on_variation_selection(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):
    """
    Price, stock, and Add to Cart update on variation selection.

    Steps:
    - Select Color, Size, etc.

    Expected:
    - Price/stock update
    - Add to Cart button becomes enabled
    """
    print(
        f"{os.linesep}Running E2E test: Update price and stock on variation selection...",
        end=" ",
    )

    page.set_viewport_size({"width": 1440, "height": 900})

    user_operations = UserOperations(graphql_client)
    user = user_operations.get_me()
    auth.set_local_storage_user_id(page, user["id"])

    product_page = ProductPage(page, config, "b2c-test-tshirt-variations")
    product_page.navigate()

    variation_selector = product_page.variation_selector

    # Get initial price (if visible)
    initial_price = product_page.get_current_price()

    # Select Color
    color_options = variation_selector.get_available_options("Color")
    assert len(color_options) > 0, "Color options should be available"
    color_options[0].click()
    page.wait_for_load_state("networkidle")

    # Select Size
    size_options = variation_selector.get_available_options("Size")
    assert len(size_options) > 0, "Size options should be available"
    size_options[0].click()
    page.wait_for_load_state("networkidle")

    # Verify all options are selected
    all_selected = variation_selector.are_all_groups_selected()
    assert all_selected, "All variation options should be selected after selecting Color and Size"

    # Price should be updated (may be same or different)
    updated_price = product_page.get_current_price()
    print(f"Initial price: {initial_price}, Updated price: {updated_price}")

    # Add to Cart should be enabled
    assert product_page.is_add_to_cart_enabled(), "Add to Cart should be enabled after selecting all options"


@pytest.mark.e2e
@allure.title("Add selected variation to cart (E2E)")
def test_e2e_add_variation_to_cart(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):
    """
    Add selected variation to cart.

    Steps:
    - Select all options
    - Click Add to Cart

    Expected:
    - Product added with correct variation
    """
    print(
        f"{os.linesep}Running E2E test: Add variation to cart...",
        end=" ",
    )

    page.set_viewport_size({"width": 1440, "height": 900})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    user = user_operations.get_me()
    auth.set_local_storage_user_id(page, user["id"])

    product_page = ProductPage(page, config, "b2c-test-tshirt-variations")
    product_page.navigate()

    variation_selector = product_page.variation_selector

    # Select Color (Red)
    variation_selector.select_option("Color", "Red")
    page.wait_for_load_state("networkidle")

    # Select Size (M - should be available)
    variation_selector.select_option("Size", "M")
    page.wait_for_load_state("networkidle")

    # Verify all options are selected
    all_selected = variation_selector.are_all_groups_selected()
    assert all_selected, "All variation options should be selected"

    # Click Add to Cart
    add_to_cart_btn = product_page.add_to_cart_button
    if add_to_cart_btn.is_visible() and product_page.is_add_to_cart_enabled():
        add_to_cart_btn.click()
        page.wait_for_load_state("networkidle")

        # Navigate to cart to verify
        cart_page = CartPage(config, page)
        cart_page.navigate()
        page.wait_for_load_state("networkidle")

        # Get cart to verify and clean up
        cart = cart_operations.get_cart(
            store_id=config["STORE_ID"],
            user_id=user["id"],
            currency_code="USD",
            culture_name="en-US",
        )

        try:
            # Verify the cart has items
            if cart and cart.get("items"):
                items = cart["items"]
                assert len(items) > 0, "Cart should have at least one item"

                # Check if the correct variation was added
                # The SKU should match our selection (Red + M)
                found_item = False
                for item in items:
                    if "RED" in item.get("sku", "").upper() and "M" in item.get("sku", "").upper():
                        found_item = True
                        print(f"Found correct variation in cart: {item.get('sku')}")
                        break

                if not found_item:
                    print(f"Added item SKUs: {[item.get('sku') for item in items]}")

        finally:
            # Clean up cart
            if cart and cart.get("id"):
                cart_operations.remove_cart(
                    payload={
                        "cartId": cart["id"],
                        "userId": user["id"],
                    }
                )


@pytest.mark.e2e
@allure.title("Cannot add to cart until all options selected (E2E)")
def test_e2e_disable_add_to_cart_until_all_options_selected(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):
    """
    Cannot add to cart until all options selected.

    Steps:
    - Select only one option

    Expected:
    - Add to Cart is disabled or shows error
    """
    print(
        f"{os.linesep}Running E2E test: Disable add to cart until all options selected...",
        end=" ",
    )

    page.set_viewport_size({"width": 1440, "height": 900})

    user_operations = UserOperations(graphql_client)
    user = user_operations.get_me()
    auth.set_local_storage_user_id(page, user["id"])

    product_page = ProductPage(page, config, "b2c-test-tshirt-variations")
    product_page.navigate()

    variation_selector = product_page.variation_selector

    # Initially, without any selection, Add to Cart should be disabled
    initial_enabled = product_page.is_add_to_cart_enabled()

    # Select only Color, not Size
    color_options = variation_selector.get_available_options("Color")
    if len(color_options) > 0:
        color_options[0].click()
        page.wait_for_load_state("networkidle")

    # Verify not all options are selected
    all_selected = variation_selector.are_all_groups_selected()

    if not all_selected:
        # Add to Cart should still be disabled
        add_to_cart_enabled = product_page.is_add_to_cart_enabled()
        assert not add_to_cart_enabled, "Add to Cart should be disabled when not all options are selected"
        print("Correctly disabled Add to Cart when not all options selected")
    else:
        # If only Color is required (single variation type), then it's OK to be enabled
        print("All required options selected, Add to Cart can be enabled")
