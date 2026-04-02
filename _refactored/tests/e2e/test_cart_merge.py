from typing import Any

import pytest
from core.auth import AuthProvider
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import CartOperations
from page_objects.pages import CartPage, SignInPage
from playwright.sync_api import Page, expect
from tests.context import Context

_PRODUCT_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"
_QUANTITY = 3
_USERNAME = "acme_store_employee_1@acme.com"


def _cleanup_user_cart(
    global_settings: GlobalSettings,
    dataset: dict[str, list[dict[str, Any]]],
    ctx: Context,
) -> None:
    user_ctx = Context.from_dataset(dataset, global_settings.store_id, _USERNAME)
    admin = AuthProvider(global_settings)
    admin.sign_in(global_settings.admin_username, global_settings.admin_password)
    with GraphQLClient(auth=admin, global_settings=global_settings) as client:
        cart_ops = CartOperations(client)
        cart = cart_ops.get_cart(
            store_id=ctx.store_id,
            user_id=user_ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
        )
        if cart:
            cart_ops.delete_cart(cart_id=cart.id, user_id=user_ctx.user_id)


@pytest.mark.e2e
@pytest.mark.quantity_control("stepper")
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
def test_cart_merge_stepper(
    global_settings: GlobalSettings,
    page: Page,
    ctx: Context,
    dataset: dict[str, list[dict[str, Any]]],
) -> None:
    try:
        cart_page = CartPage(global_settings=global_settings, page=page)
        cart_page.navigate()

        line_item = cart_page.find_line_item(sku=_PRODUCT_ID)
        expect(line_item.root).to_be_visible()

        sign_in_page = SignInPage(global_settings=global_settings, page=page)
        sign_in_page.navigate()

        sign_in_page.email_input.fill(_USERNAME)
        sign_in_page.password_input.fill(
            global_settings.users_password.get_secret_value()
        )
        sign_in_page.sign_in_button.click()

        cart_page.navigate()
        line_item = cart_page.find_line_item(sku=_PRODUCT_ID)
        expect(line_item.root).to_be_visible()
        expect(line_item.quantity_stepper.quantity_input).to_have_value(str(_QUANTITY))
    finally:
        _cleanup_user_cart(global_settings, dataset, ctx)


@pytest.mark.e2e
@pytest.mark.quantity_control("button")
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
def test_cart_merge_button(
    global_settings: GlobalSettings,
    page: Page,
    ctx: Context,
    dataset: dict[str, list[dict[str, Any]]],
) -> None:
    try:
        cart_page = CartPage(global_settings=global_settings, page=page)
        cart_page.navigate()

        line_item = cart_page.find_line_item(sku=_PRODUCT_ID)
        expect(line_item.root).to_be_visible()

        sign_in_page = SignInPage(global_settings=global_settings, page=page)
        sign_in_page.navigate()

        sign_in_page.email_input.fill(_USERNAME)
        sign_in_page.password_input.fill(
            global_settings.users_password.get_secret_value()
        )
        sign_in_page.sign_in_button.click()

        cart_page.navigate()
        line_item = cart_page.find_line_item(sku=_PRODUCT_ID)
        expect(line_item.root).to_be_visible()
        expect(line_item.add_to_cart_button.quantity_input).to_have_value(str(_QUANTITY))
    finally:
        _cleanup_user_cart(global_settings, dataset, ctx)
