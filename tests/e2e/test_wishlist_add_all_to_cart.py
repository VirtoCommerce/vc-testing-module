from uuid import uuid4

import allure
import pytest
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import CartOperations, ShoppingListOperations
from gql.types.cart_item_input import CartItemInput
from page_objects.pages import AccountListDetailsPage, CartPage
from playwright.sync_api import Page, Response, expect
from tests.context import Context
from utils.polling_utils import poll_until

_USERNAME = "acme_store_employee_1@acme.com"
_PHYSICAL_PRODUCT_ID = "smartphone-samsung-galaxy-a57-5g"
_PHYSICAL_PRODUCT_SKU = "smartphone-samsung-galaxy-a57-5g"
_VARIATION_PRODUCT_ID = "smartphone-google-pixel-10-indigo"
_VARIATION_PRODUCT_SKU = "smartphone-google-pixel-10-indigo"


def _is_cart_from_wishlist_mutation(response: Response) -> bool:
    if "/graphql" not in response.url:
        return False
    post = (response.request.post_data or "").lower()
    return "mutation" in post and "cart" in post


@pytest.mark.e2e
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Wishlist / Add products to cart (E2E)")
@allure.title("Add all wishlist products to cart from list details")
def test_wishlist_add_all_products_to_cart(
    page: Page,
    global_settings: GlobalSettings,
    graphql_client: GraphQLClient,
    ctx: Context,
) -> None:
    ops = ShoppingListOperations(client=graphql_client)
    cart_ops = CartOperations(client=graphql_client)
    wishlist = ops.create_shopping_list(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        name=f"E2E WL Cart {uuid4().hex[:6]}",
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
        description="Created by wishlist add-to-cart E2E flow",
    )
    try:
        expected_skus = {_PHYSICAL_PRODUCT_SKU, _VARIATION_PRODUCT_SKU}
        ops.add_items_to_shopping_list(
            list_id=wishlist.id,
            items=[
                CartItemInput(product_id=_PHYSICAL_PRODUCT_ID, quantity=1),
                CartItemInput(product_id=_VARIATION_PRODUCT_ID, quantity=1),
            ],
        )
        seeded = poll_until(
            fetch=lambda: ops.get_shopping_list(list_id=wishlist.id, culture_name=ctx.culture_name),
            predicate=lambda wl: expected_skus.issubset({item.sku for item in wl.items}),
            attempts=global_settings.poll_attempts,
            interval=global_settings.poll_interval,
        )
        assert seeded is not None, "Seeded products did not appear in wishlist"

        with allure.step("Open wishlist details and verify seeded products are shown"):
            details_page = AccountListDetailsPage(global_settings=global_settings, page=page, list_id=wishlist.id)
            details_page.navigate()
            expect(details_page.line_items).to_have_count(2)
            expect(details_page.find_line_item(_PHYSICAL_PRODUCT_SKU).root).to_be_visible()
            expect(details_page.find_line_item(_VARIATION_PRODUCT_SKU).root).to_be_visible()

        with allure.step("Add all wishlist products to cart and verify cart contents"):
            with page.expect_response(_is_cart_from_wishlist_mutation):
                details_page.add_all_to_cart_button.click()
            expect(details_page.cart_quantity_label).to_have_text("2")

            cart_page = CartPage(global_settings=global_settings, page=page)
            cart_page.navigate()
            expect(cart_page.line_items).to_have_count(2)
            expect(cart_page.find_line_item(_PHYSICAL_PRODUCT_SKU).root).to_be_visible()
            expect(cart_page.find_line_item(_VARIATION_PRODUCT_SKU).root).to_be_visible()
    finally:
        try:
            ops.delete_shopping_list(list_id=wishlist.id)
        except Exception as exc:
            allure.attach(
                f"Teardown of wishlist {wishlist.id} skipped: {exc}",
                name=f"wishlist-teardown-{wishlist.id}",
                attachment_type=allure.attachment_type.TEXT,
            )
        try:
            cart = cart_ops.get_cart(
                store_id=ctx.store_id,
                user_id=ctx.user_id,
                currency_code=ctx.currency_code,
                culture_name=ctx.culture_name,
            )
            if cart:
                cart_ops.delete_cart(cart_id=cart.id, user_id=ctx.user_id)
        except Exception as exc:
            allure.attach(
                f"Cart teardown skipped: {exc}",
                name="cart-teardown",
                attachment_type=allure.attachment_type.TEXT,
            )
