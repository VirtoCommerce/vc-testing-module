from collections.abc import Callable
from uuid import uuid4

import allure
import pytest
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import ShoppingListOperations
from page_objects.components import AddToWishlistsModal
from page_objects.pages import CategoryPage, ProductPage
from playwright.sync_api import Page, Response, expect
from tests.context import Context
from utils.polling_utils import poll_until

_USERNAME = "acme_store_employee_1@acme.com"
_CATEGORY_PATH = "smartphones"
_PHYSICAL_PRODUCT_SKU = "smartphone-samsung-galaxy-a57-5g"
_VARIATION_PARENT_SKU = "smartphone-google-pixel-10-frost"
_VARIATION_PRODUCT_ID = "smartphone-google-pixel-10-indigo"
_VARIATION_PRODUCT_SKU = "smartphone-google-pixel-10-indigo"


def _is_wishlist_item_mutation(response: Response) -> bool:
    if "/graphql" not in response.url:
        return False
    post = (response.request.post_data or "").lower()
    return "mutation" in post and "wishlist" in post


def _open_from_grid(page: Page, global_settings: GlobalSettings) -> str:
    category_page = CategoryPage(global_settings=global_settings, page=page, path=_CATEGORY_PATH)
    category_page.navigate()
    card = category_page.scroll_to_product(_PHYSICAL_PRODUCT_SKU)
    expect(card.add_to_list_button).to_be_visible()
    card.add_to_list_button.click()
    return _PHYSICAL_PRODUCT_SKU


def _open_from_list_view(page: Page, global_settings: GlobalSettings) -> str:
    category_page = CategoryPage(global_settings=global_settings, page=page, path=_CATEGORY_PATH)
    category_page.navigate()
    category_page.view_switcher.list_view_tab.click()
    card = category_page.scroll_to_product(_VARIATION_PARENT_SKU)
    expect(card.add_to_list_button).to_be_visible()
    card.add_to_list_button.click()
    return _VARIATION_PARENT_SKU


def _open_from_pdp(page: Page, global_settings: GlobalSettings) -> str:
    product_page = ProductPage(global_settings=global_settings, page=page, product_id=_VARIATION_PRODUCT_ID)
    product_page.navigate()
    expect(product_page.add_to_list_button).to_be_visible()
    product_page.add_to_list_button.click()
    return _VARIATION_PRODUCT_SKU


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.parametrize(
    "open_add_to_list,source_label",
    [
        (_open_from_grid, "grid view"),
        (_open_from_list_view, "list view"),
        (_open_from_pdp, "product detail page"),
    ],
    ids=["grid-view", "list-view", "product-detail-page"],
)
@allure.feature("Wishlist / Add product (E2E)")
@allure.title("Add a product to a wishlist from {source_label}")
def test_wishlist_add_product(
    page: Page,
    global_settings: GlobalSettings,
    graphql_client: GraphQLClient,
    ctx: Context,
    open_add_to_list: Callable[[Page, GlobalSettings], str],
    source_label: str,
) -> None:
    ops = ShoppingListOperations(client=graphql_client)
    wishlist = ops.create_shopping_list(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        name=f"E2E WL Add {source_label[:8]} {uuid4().hex[:6]}",
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
        description=f"Created by wishlist E2E add-from-{source_label} flow",
    )
    try:
        expected_sku = open_add_to_list(page, global_settings)

        with allure.step(f"Select wishlist in modal and save (source: {source_label})"):
            modal = AddToWishlistsModal(root=page.locator("[data-test-id='add-to-wishlists-modal']"))
            expect(modal.root).to_be_visible()
            modal.list_checkbox(wishlist.id).click()
            with page.expect_response(_is_wishlist_item_mutation):
                modal.save_button.click()
            expect(modal.root).not_to_be_visible()

        with allure.step(f"Verify product '{expected_sku}' appears in the wishlist"):
            updated = poll_until(
                fetch=lambda: ops.get_shopping_list(list_id=wishlist.id, culture_name=ctx.culture_name),
                predicate=lambda wl: expected_sku in {item.sku for item in wl.items},
                attempts=global_settings.poll_attempts,
                interval=global_settings.poll_interval,
            )
            assert updated is not None, f"Product '{expected_sku}' did not appear in wishlist {wishlist.id}"
    finally:
        ops.delete_shopping_list(list_id=wishlist.id)
