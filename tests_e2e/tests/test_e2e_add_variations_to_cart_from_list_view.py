"""
E2E tests for adding and updating product variations in cart from the category list view.

Test Cases:
- test_e2e_add_variation_to_cart_from_list_view_stepper: Switch to list view, expand variations,
  add two variations to cart using stepper, and verify cart badge and count-in-cart labels.
- test_e2e_add_variation_to_cart_from_list_view_button: Same flow using add-to-cart button.
- test_e2e_update_variation_quantity_from_list_view_stepper: Switch to list view, expand variations,
  add a variation to cart using stepper, increment and decrement quantity, verify updates.
- test_e2e_update_variation_quantity_from_list_view_button: Same flow using add-to-cart button.
"""

import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import CartPage, CategoryPage

SMART_WATCHES_SEO_PATH = "smart-watches"
PRODUCT_SKU = "B2B-SIMPLE-001"
VARIATION_NAME_RED = "B2B Simple Product - Red"
VARIATION_NAME_BLUE = "B2B Simple Product - Blue"


@pytest.mark.e2e
@pytest.mark.quantity_control("stepper")
@allure.title("Add variations to cart from category list view with stepper (E2E)")
def test_e2e_add_variation_to_cart_from_list_view_stepper(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(f"{os.linesep}Running E2E test to add variations to cart from list view with stepper...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    with allure.step("Authenticate as regular user"):
        dataset_user = dataset["users"][0]
        auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"], page)
        user = user_operations.get_me()

    with allure.step("Navigate to Smart Watches category and switch to list view"):
        category_page = CategoryPage(config, page, SMART_WATCHES_SEO_PATH)
        category_page.navigate()

        category_page.view_switcher.switch_category_view("list")
        page.wait_for_load_state("networkidle")

        expect(
            category_page.products_list_view,
            "Products list view should be visible after switching to list view",
        ).to_be_visible()

    with allure.step(f"Find product card for SKU {PRODUCT_SKU} and expand variations"):
        product_card = category_page.get_product_card_by_sku_list(PRODUCT_SKU)
        assert product_card is not None, f"Product card with SKU '{PRODUCT_SKU}' not found in list view"

        expect(
            product_card.variations_button,
            "Variations button should be visible on the product card in list view",
        ).to_be_visible()

        product_card.variations_button.click()
        page.wait_for_load_state("networkidle")

        expect(
            product_card.variants_wrapper,
            "Variants wrapper should be visible after clicking the variations button",
        ).to_be_visible()

        expect(
            product_card.variants_wrapper.locator("[data-test-id='line-item']").first,
            "At least one variation line item should be visible",
        ).to_be_visible()

    try:
        with allure.step(f"Add '{VARIATION_NAME_RED}' to cart"):
            variation_red = product_card.get_variation_line_item_by_name(VARIATION_NAME_RED)
            assert variation_red is not None, f"Variation line item '{VARIATION_NAME_RED}' not found"

            variation_red.quantity_stepper_increment.click()
            page.wait_for_load_state("networkidle")

            expect(
                variation_red.count_in_cart_label,
                f"Count in cart label should be visible for '{VARIATION_NAME_RED}'",
            ).to_be_visible()
            expect(
                variation_red.count_in_cart_label,
                f"Count in cart label should show '1' for '{VARIATION_NAME_RED}'",
            ).to_have_text("1")

        with allure.step(f"Add '{VARIATION_NAME_BLUE}' to cart"):
            variation_blue = product_card.get_variation_line_item_by_name(VARIATION_NAME_BLUE)
            assert variation_blue is not None, f"Variation line item '{VARIATION_NAME_BLUE}' not found"

            variation_blue.quantity_stepper_increment.click()
            page.wait_for_load_state("networkidle")

            expect(
                variation_blue.count_in_cart_label,
                f"Count in cart label should be visible for '{VARIATION_NAME_BLUE}'",
            ).to_be_visible()
            expect(
                variation_blue.count_in_cart_label,
                f"Count in cart label should show '1' for '{VARIATION_NAME_BLUE}'",
            ).to_have_text("1")

        with allure.step("Verify cart badge shows 2 items"):
            expect(
                category_page.cart_badge,
                "Cart badge should show '2' after adding two variations",
            ).to_have_text("2")

    finally:
        with allure.step("Cleanup: remove cart"):
            cart = cart_operations.get_cart(
                store_id=config["STORE_ID"],
                user_id=user["id"],
                currency_code="USD",
                culture_name="en-US",
            )
            if cart and cart.get("id"):
                cart_operations.remove_cart(
                    payload={
                        "cartId": cart["id"],
                        "userId": user["id"],
                    }
                )
            auth.clear_token()


@pytest.mark.e2e
@pytest.mark.quantity_control("button")
@allure.title("Add variations to cart from category list view with button (E2E)")
def test_e2e_add_variation_to_cart_from_list_view_button(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(f"{os.linesep}Running E2E test to add variations to cart from list view with button...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    with allure.step("Authenticate as regular user"):
        dataset_user = dataset["users"][0]
        auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"], page)
        user = user_operations.get_me()

    with allure.step("Navigate to Smart Watches category and switch to list view"):
        category_page = CategoryPage(config, page, SMART_WATCHES_SEO_PATH)
        category_page.navigate()

        category_page.view_switcher.switch_category_view("list")
        page.wait_for_load_state("networkidle")

        expect(
            category_page.products_list_view,
            "Products list view should be visible after switching to list view",
        ).to_be_visible()

    with allure.step(f"Find product card for SKU {PRODUCT_SKU} and expand variations"):
        product_card = category_page.get_product_card_by_sku_list(PRODUCT_SKU)
        assert product_card is not None, f"Product card with SKU '{PRODUCT_SKU}' not found in list view"

        expect(
            product_card.variations_button,
            "Variations button should be visible on the product card in list view",
        ).to_be_visible()

        product_card.variations_button.click()
        page.wait_for_load_state("networkidle")

        expect(
            product_card.variants_wrapper,
            "Variants wrapper should be visible after clicking the variations button",
        ).to_be_visible()

        expect(
            product_card.variants_wrapper.locator("[data-test-id='line-item']").first,
            "At least one variation line item should be visible",
        ).to_be_visible()

    try:
        with allure.step(f"Add '{VARIATION_NAME_RED}' to cart"):
            variation_red = product_card.get_variation_line_item_by_name(VARIATION_NAME_RED)
            assert variation_red is not None, f"Variation line item '{VARIATION_NAME_RED}' not found"

            variation_red.add_to_cart_component.add_to_cart_text_button.click()
            page.wait_for_load_state("networkidle")

            expect(
                variation_red.count_in_cart_label,
                f"Count in cart label should be visible for '{VARIATION_NAME_RED}'",
            ).to_be_visible()
            expect(
                variation_red.count_in_cart_label,
                f"Count in cart label should show '1' for '{VARIATION_NAME_RED}'",
            ).to_have_text("1")

        with allure.step(f"Add '{VARIATION_NAME_BLUE}' to cart"):
            variation_blue = product_card.get_variation_line_item_by_name(VARIATION_NAME_BLUE)
            assert variation_blue is not None, f"Variation line item '{VARIATION_NAME_BLUE}' not found"

            variation_blue.add_to_cart_component.add_to_cart_text_button.click()
            page.wait_for_load_state("networkidle")

            expect(
                variation_blue.count_in_cart_label,
                f"Count in cart label should be visible for '{VARIATION_NAME_BLUE}'",
            ).to_be_visible()
            expect(
                variation_blue.count_in_cart_label,
                f"Count in cart label should show '1' for '{VARIATION_NAME_BLUE}'",
            ).to_have_text("1")

        with allure.step("Verify cart badge shows 2 items"):
            expect(
                category_page.cart_badge,
                "Cart badge should show '2' after adding two variations",
            ).to_have_text("2")

    finally:
        with allure.step("Cleanup: remove cart"):
            cart = cart_operations.get_cart(
                store_id=config["STORE_ID"],
                user_id=user["id"],
                currency_code="USD",
                culture_name="en-US",
            )
            if cart and cart.get("id"):
                cart_operations.remove_cart(
                    payload={
                        "cartId": cart["id"],
                        "userId": user["id"],
                    }
                )
            auth.clear_token()


@pytest.mark.e2e
@pytest.mark.quantity_control("stepper")
@allure.title("Update variation quantity in cart from category list view with stepper (E2E)")
def test_e2e_update_variation_quantity_from_list_view_stepper(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(f"{os.linesep}Running E2E test to update variation quantity from list view with stepper...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    with allure.step("Authenticate as regular user"):
        dataset_user = dataset["users"][0]
        auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"], page)
        user = user_operations.get_me()

    with allure.step("Navigate to Smart Watches category and switch to list view"):
        category_page = CategoryPage(config, page, SMART_WATCHES_SEO_PATH)
        category_page.navigate()

        category_page.view_switcher.switch_category_view("list")
        page.wait_for_load_state("networkidle")

        expect(
            category_page.products_list_view,
            "Products list view should be visible after switching to list view",
        ).to_be_visible()

    with allure.step(f"Find product card for SKU {PRODUCT_SKU} and expand variations"):
        product_card = category_page.get_product_card_by_sku_list(PRODUCT_SKU)
        assert product_card is not None, f"Product card with SKU '{PRODUCT_SKU}' not found in list view"

        expect(
            product_card.variations_button,
            "Variations button should be visible on the product card in list view",
        ).to_be_visible()

        product_card.variations_button.click()
        page.wait_for_load_state("networkidle")

        expect(
            product_card.variants_wrapper.locator("[data-test-id='line-item']").first,
            "At least one variation line item should be visible",
        ).to_be_visible()

    try:
        with allure.step(f"Add '{VARIATION_NAME_RED}' to cart (quantity 1)"):
            variation_red = product_card.get_variation_line_item_by_name(VARIATION_NAME_RED)
            assert variation_red is not None, f"Variation line item '{VARIATION_NAME_RED}' not found"

            variation_red.quantity_stepper_increment.click()
            page.wait_for_load_state("networkidle")

            expect(variation_red.quantity_input, "Quantity input should show '1'").to_have_value("1")
            expect(variation_red.count_in_cart_label, "Count in cart should show '1'").to_have_text("1")

        with allure.step(f"Increment '{VARIATION_NAME_RED}' quantity to 2"):
            variation_red.quantity_stepper_increment.click()
            page.wait_for_load_state("networkidle")

            expect(variation_red.quantity_input, "Quantity input should show '2'").to_have_value("2")
            expect(variation_red.count_in_cart_label, "Count in cart should show '2'").to_have_text("2")

        with allure.step(f"Decrement '{VARIATION_NAME_RED}' quantity back to 1"):
            variation_red.quantity_stepper_decrement.click()
            page.wait_for_load_state("networkidle")

            expect(variation_red.quantity_input, "Quantity input should show '1'").to_have_value("1")
            expect(variation_red.count_in_cart_label, "Count in cart should show '1'").to_have_text("1")

        with allure.step("Verify cart badge shows 1 item"):
            expect(
                category_page.cart_badge,
                "Cart badge should show '1' after updating variation quantity",
            ).to_have_text("1")

    finally:
        with allure.step("Cleanup: remove cart"):
            cart = cart_operations.get_cart(
                store_id=config["STORE_ID"],
                user_id=user["id"],
                currency_code="USD",
                culture_name="en-US",
            )
            if cart and cart.get("id"):
                cart_operations.remove_cart(
                    payload={
                        "cartId": cart["id"],
                        "userId": user["id"],
                    }
                )
            auth.clear_token()


@pytest.mark.e2e
@pytest.mark.quantity_control("button")
@allure.title("Update variation quantity in cart from category list view with button (E2E)")
def test_e2e_update_variation_quantity_from_list_view_button(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(f"{os.linesep}Running E2E test to update variation quantity from list view with button...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    with allure.step("Authenticate as regular user"):
        dataset_user = dataset["users"][0]
        auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"], page)
        user = user_operations.get_me()

    with allure.step("Navigate to Smart Watches category and switch to list view"):
        category_page = CategoryPage(config, page, SMART_WATCHES_SEO_PATH)
        category_page.navigate()

        category_page.view_switcher.switch_category_view("list")
        page.wait_for_load_state("networkidle")

        expect(
            category_page.products_list_view,
            "Products list view should be visible after switching to list view",
        ).to_be_visible()

    with allure.step(f"Find product card for SKU {PRODUCT_SKU} and expand variations"):
        product_card = category_page.get_product_card_by_sku_list(PRODUCT_SKU)
        assert product_card is not None, f"Product card with SKU '{PRODUCT_SKU}' not found in list view"

        expect(
            product_card.variations_button,
            "Variations button should be visible on the product card in list view",
        ).to_be_visible()

        product_card.variations_button.click()
        page.wait_for_load_state("networkidle")

        expect(
            product_card.variants_wrapper.locator("[data-test-id='line-item']").first,
            "At least one variation line item should be visible",
        ).to_be_visible()

    try:
        with allure.step(f"Add '{VARIATION_NAME_RED}' to cart (quantity 1)"):
            variation_red = product_card.get_variation_line_item_by_name(VARIATION_NAME_RED)
            assert variation_red is not None, f"Variation line item '{VARIATION_NAME_RED}' not found"

            variation_red.add_to_cart_component.add_to_cart_text_button.click()
            page.wait_for_load_state("networkidle")

            expect(variation_red.quantity_input, "Quantity input should show '1'").to_have_value("1")
            expect(variation_red.count_in_cart_label, "Count in cart should show '1'").to_have_text("1")

        with allure.step(f"Increment '{VARIATION_NAME_RED}' quantity to 2"):
            variation_red.add_to_cart_component.quantity_input.fill("2")
            variation_red.add_to_cart_component.add_to_cart_text_button.click()
            page.wait_for_load_state("networkidle")

            expect(variation_red.quantity_input, "Quantity input should show '2'").to_have_value("2")
            expect(variation_red.count_in_cart_label, "Count in cart should show '2'").to_have_text("2")

        with allure.step(f"Decrement '{VARIATION_NAME_RED}' quantity back to 1"):
            variation_red.add_to_cart_component.quantity_input.fill("1")
            variation_red.add_to_cart_component.add_to_cart_text_button.click()
            page.wait_for_load_state("networkidle")

            expect(variation_red.quantity_input, "Quantity input should show '1'").to_have_value("1")
            expect(variation_red.count_in_cart_label, "Count in cart should show '1'").to_have_text("1")

        with allure.step("Verify cart badge shows 1 item"):
            expect(
                category_page.cart_badge,
                "Cart badge should show '1' after updating variation quantity",
            ).to_have_text("1")

    finally:
        with allure.step("Cleanup: remove cart"):
            cart = cart_operations.get_cart(
                store_id=config["STORE_ID"],
                user_id=user["id"],
                currency_code="USD",
                culture_name="en-US",
            )
            if cart and cart.get("id"):
                cart_operations.remove_cart(
                    payload={
                        "cartId": cart["id"],
                        "userId": user["id"],
                    }
                )
            auth.clear_token()
