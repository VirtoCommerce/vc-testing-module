import time
from typing import Any

import allure
import pytest
from core.auth import AuthProvider
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import CartOperations
from gql.types.cart_item_input import CartItemInput
from page_objects.frontend.pages import CartPage, ProductPage, SignInPage
from playwright.sync_api import Page, expect
from tests.context import Context

_REGULAR_PRODUCT_ID = "smartphone-samsung-galaxy-a57-5g"
_REGULAR_QUANTITY = 2
_CONFIGURABLE_PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai"
_CONFIGURABLE_PRODUCT_PATH = "laptops/acer-predator-helios-neo-16-ai"
_CONFIGURED_SKU = f"Configuration-{_CONFIGURABLE_PRODUCT_ID}"
_MEMORY_SECTION_NAME = "Memory"
_MEMORY_OPTION_NAME = "Samsung DDR5-4800 8GB"
_USERNAME = "acme_store_employee_1@acme.com"


def _user_provider(global_settings: GlobalSettings) -> AuthProvider:
    provider = AuthProvider(global_settings.backend_base_url)
    provider.sign_in(_USERNAME, global_settings.users_password)
    return provider


def _delete_user_cart(global_settings: GlobalSettings, user_ctx: Context) -> None:
    """Delete the registered user's cart via the user's own auth.

    Admin auth cannot read this user's storefront cart, so cleanup must run
    as the user to reliably find and remove the cart between runs.
    """
    provider = _user_provider(global_settings)
    try:
        with GraphQLClient(auth=provider, global_settings=global_settings) as client:
            cart_ops = CartOperations(client)
            cart = cart_ops.get_cart(
                store_id=user_ctx.store_id,
                user_id=user_ctx.user_id,
                currency_code=user_ctx.currency_code,
                culture_name=user_ctx.culture_name,
            )
            if cart:
                cart_ops.delete_cart(cart_id=cart.id, user_id=user_ctx.user_id)
    finally:
        if provider.is_authenticated:
            provider.sign_out()


def _seed_user_cart(global_settings: GlobalSettings, user_ctx: Context) -> None:
    """Seed the user's cart with a regular product and wait until it is
    read-back-visible so the later storefront merge includes it."""
    provider = _user_provider(global_settings)
    try:
        with GraphQLClient(auth=provider, global_settings=global_settings) as client:
            cart_ops = CartOperations(client)
            cart_ops.add_items_to_cart(
                store_id=user_ctx.store_id,
                user_id=user_ctx.user_id,
                items=[CartItemInput(product_id=_REGULAR_PRODUCT_ID, quantity=_REGULAR_QUANTITY)],
                currency_code=user_ctx.currency_code,
                culture_name=user_ctx.culture_name,
            )
            for _ in range(global_settings.poll_attempts):
                cart = cart_ops.get_cart(
                    store_id=user_ctx.store_id,
                    user_id=user_ctx.user_id,
                    currency_code=user_ctx.currency_code,
                    culture_name=user_ctx.culture_name,
                )
                items = cart.items if cart else None
                if items and any(i.sku == _REGULAR_PRODUCT_ID for i in items):
                    break
                time.sleep(global_settings.poll_interval)
    finally:
        if provider.is_authenticated:
            provider.sign_out()


@pytest.mark.e2e
@allure.feature("Cart / Merge (E2E)")
@allure.title("Anonymous configured product merges into the signed-in cart holding a regular product")
def test_cart_merge_configured_and_regular(
    global_settings: GlobalSettings,
    page: Page,
    dataset: dict[str, list[dict[str, Any]]],
) -> None:
    user_ctx = Context.from_dataset(dataset, global_settings.store_id, _USERNAME)
    try:
        with allure.step("Ensure the registered user starts with an empty cart"):
            _delete_user_cart(global_settings, user_ctx)

        with allure.step(f"Seed the registered user's cart with regular product '{_REGULAR_PRODUCT_ID}'"):
            _seed_user_cart(global_settings, user_ctx)

        with allure.step("As anonymous user, configure a product and add it to the cart"):
            product_page = ProductPage(
                global_settings=global_settings,
                page=page,
                path=_CONFIGURABLE_PRODUCT_PATH,
            )
            product_page.navigate()
            expect(product_page.product_configuration_area.root).to_be_visible()
            product_page.product_configuration_area.select_option(
                section_name=_MEMORY_SECTION_NAME, option_name=_MEMORY_OPTION_NAME
            )
            product_page.add_to_cart()
            expect(product_page.cart_quantity_label).to_have_text("1")

        with allure.step(f"Sign in as {_USERNAME}"):
            sign_in_page = SignInPage(global_settings=global_settings, page=page)
            sign_in_page.navigate()
            sign_in_page.email_input.fill(_USERNAME)
            sign_in_page.password_input.fill(global_settings.users_password.get_secret_value())
            sign_in_page.sign_in_button.click()
            # Sign-in redirects away from the form; wait for it so the anonymous
            # cart has been merged into the user cart before we assert on it.
            page.wait_for_url(lambda url: "/sign-in" not in url, timeout=15000)

        with allure.step("Open the cart and verify both the regular and configured products are present"):
            cart_page = CartPage(global_settings=global_settings, page=page)
            cart_page.navigate()

            # The storefront merges the carts a moment after sign-in; wait for the
            # merged state (both line items present) before asserting on each one.
            expect(cart_page.line_items).to_have_count(2, timeout=15000)

            regular_item = cart_page.find_line_item(sku=_REGULAR_PRODUCT_ID)
            expect(regular_item.root).to_be_visible()

            configured_item = cart_page.find_line_item(sku=_CONFIGURED_SKU)
            expect(configured_item.root).to_be_visible()
    finally:
        _delete_user_cart(global_settings, user_ctx)
