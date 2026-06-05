from uuid import uuid4

import allure
import pytest
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import ShoppingListOperations
from gql.types.cart_item_input import CartItemInput
from page_objects.components import AddToWishlistsModal
from page_objects.pages import CategoryPage
from playwright.sync_api import Page, Response, expect
from tests.context import Context
from utils.polling_utils import poll_until

_USERNAME = "acme_store_employee_1@acme.com"
_CATEGORY_PATH = "smartphones"
_PHYSICAL_PRODUCT_ID = "smartphone-samsung-galaxy-a57-5g"
_PHYSICAL_PRODUCT_SKU = "smartphone-samsung-galaxy-a57-5g"


def _is_wishlist_item_mutation(response: Response) -> bool:
    if "/graphql" not in response.url:
        return False
    post = (response.request.post_data or "").lower()
    return "mutation" in post and "wishlist" in post


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@allure.feature("Wishlist / Remove product (E2E)")
@allure.title("Remove a product from a wishlist via the add-to-list modal")
def test_wishlist_remove_product_via_add_to_list_modal(
    page: Page,
    global_settings: GlobalSettings,
    graphql_client: GraphQLClient,
    ctx: Context,
) -> None:
    ops = ShoppingListOperations(client=graphql_client)
    wishlist = ops.create_shopping_list(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        name=f"E2E WL Remove {uuid4().hex[:6]}",
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
        description="Created by wishlist E2E remove-via-modal flow",
    )
    try:
        ops.add_items_to_shopping_list(
            list_id=wishlist.id,
            items=[CartItemInput(product_id=_PHYSICAL_PRODUCT_ID, quantity=1)],
        )
        seeded = poll_until(
            fetch=lambda: ops.get_shopping_list(list_id=wishlist.id, culture_name=ctx.culture_name),
            predicate=lambda wl: _PHYSICAL_PRODUCT_SKU in {item.sku for item in wl.items},
            attempts=global_settings.poll_attempts,
            interval=global_settings.poll_interval,
        )
        assert seeded is not None, "Seed product did not appear in wishlist"

        with allure.step("Open add-to-list modal for the seeded product from category grid"):
            category_page = CategoryPage(global_settings=global_settings, page=page, path=_CATEGORY_PATH)
            category_page.navigate()
            card = category_page.scroll_to_product(_PHYSICAL_PRODUCT_SKU)
            card.add_to_list_button.click()
            modal = AddToWishlistsModal(root=page.locator("[data-test-id='add-to-wishlists-modal']"))
            expect(modal.root).to_be_visible()

        with allure.step("Deselect the wishlist containing the product and save"):
            modal.list_with_product_checkbox(wishlist.id).click()
            with page.expect_response(_is_wishlist_item_mutation):
                modal.save_button.click()
            expect(modal.root).not_to_be_visible()

        with allure.step(f"Verify product '{_PHYSICAL_PRODUCT_SKU}' is removed from the wishlist"):
            removed = poll_until(
                fetch=lambda: ops.get_shopping_list(list_id=wishlist.id, culture_name=ctx.culture_name),
                predicate=lambda wl: _PHYSICAL_PRODUCT_SKU not in {item.sku for item in wl.items},
                attempts=global_settings.poll_attempts,
                interval=global_settings.poll_interval,
            )
            assert removed is not None, f"Product '{_PHYSICAL_PRODUCT_SKU}' was not removed from wishlist"
    finally:
        ops.delete_shopping_list(list_id=wishlist.id)
