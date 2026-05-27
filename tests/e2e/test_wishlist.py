import time
from typing import Generator
from uuid import uuid4

import allure
import pytest
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import CartOperations, ShoppingListOperations
from gql.types.cart_item_input import CartItemInput
from gql.types.shopping_list import ShoppingList
from page_objects.components import (
    AddOrUpdateWishlistModal,
    AddToWishlistsModal,
    DeleteWishlistModal,
)
from page_objects.pages import (
    AccountListDetailsPage,
    AccountListsPage,
    CartPage,
    CategoryPage,
    ProductPage,
)
from playwright.sync_api import Page, Response, expect
from tests.context import Context

_AUTO_PREFIX = "E2E WL"
_USERNAME = "acme_store_employee_1@acme.com"

_CATEGORY_PATH = "smartphones"
_PHYSICAL_PRODUCT_ID = "smartphone-samsung-galaxy-a57-5g"
_PHYSICAL_PRODUCT_SKU = "smartphone-samsung-galaxy-a57-5g"
_VARIATION_PARENT_SKU = "smartphone-google-pixel-10-frost"
_VARIATION_PRODUCT_ID = "smartphone-google-pixel-10-indigo"
_VARIATION_PRODUCT_SKU = "smartphone-google-pixel-10-indigo"

_SCOPE_LABELS = {
    "Private": "Private",
    "AnyoneAnonymous": "Anyone (readonly)",
    "Organization": "Organization",
}


def _is_wishlist_graphql(response: Response) -> bool:
    post = response.request.post_data or ""
    return (
        "/graphql" in response.url
        and "mutation" in post.lower()
        and "wishlist" in post.lower()
    )


def _is_cart_graphql(response: Response) -> bool:
    post = response.request.post_data or ""
    return (
        "/graphql" in response.url
        and "mutation" in post.lower()
        and "cart" in post.lower()
    )


def _unique_name(suffix: str) -> str:
    return f"{_AUTO_PREFIX} {suffix[:8]} {uuid4().hex[:6]}"


def _delete_auto_wishlists(ops: ShoppingListOperations, ctx: Context) -> None:
    for wishlist in ops.get_shopping_lists(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
    ):
        if wishlist.name.startswith(_AUTO_PREFIX) or wishlist.name.startswith(
            "E2E Wishlist"
        ):
            ops.delete_shopping_list(wishlist.id)


def _wait_for_skus(
    ops: ShoppingListOperations,
    list_id: str,
    expected_skus: set[str],
    culture_name: str,
) -> ShoppingList:
    for _ in range(10):
        wishlist = ops.get_shopping_list(list_id=list_id, culture_name=culture_name)
        actual_skus = {item.sku for item in wishlist.items}
        if expected_skus.issubset(actual_skus):
            return wishlist
        time.sleep(0.5)

    wishlist = ops.get_shopping_list(list_id=list_id, culture_name=culture_name)
    actual_skus = {item.sku for item in wishlist.items}
    raise AssertionError(f"Expected SKUs {expected_skus}, got {actual_skus}")


def _wait_for_sku_removed(
    ops: ShoppingListOperations, list_id: str, sku: str, culture_name: str
) -> ShoppingList:
    for _ in range(10):
        wishlist = ops.get_shopping_list(list_id=list_id, culture_name=culture_name)
        if sku not in {item.sku for item in wishlist.items}:
            return wishlist
        time.sleep(0.5)

    wishlist = ops.get_shopping_list(list_id=list_id, culture_name=culture_name)
    raise AssertionError(f"SKU '{sku}' was not removed from list {list_id}")


def _wait_for_scope(
    ops: ShoppingListOperations, list_id: str, expected_scope: str, culture_name: str
) -> ShoppingList:
    for _ in range(10):
        wishlist = ops.get_shopping_list(list_id=list_id, culture_name=culture_name)
        actual_scope = wishlist.sharing_setting.scope if wishlist.sharing_setting else None
        if actual_scope == expected_scope:
            return wishlist
        time.sleep(0.5)

    wishlist = ops.get_shopping_list(list_id=list_id, culture_name=culture_name)
    actual_scope = wishlist.sharing_setting.scope if wishlist.sharing_setting else None
    raise AssertionError(f"Expected scope '{expected_scope}', got '{actual_scope}'")


def _delete_cart_if_exists(cart_ops: CartOperations, ctx: Context) -> None:
    cart = cart_ops.get_cart(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
    )
    if cart:
        cart_ops.delete_cart(cart_id=cart.id, user_id=ctx.user_id)


@pytest.fixture
def wishlist_ops(
    graphql_client: GraphQLClient, ctx: Context
) -> Generator[ShoppingListOperations, None, None]:
    ops = ShoppingListOperations(graphql_client)
    _delete_auto_wishlists(ops, ctx)
    yield ops
    _delete_auto_wishlists(ops, ctx)


@pytest.fixture
def clean_cart(
    graphql_client: GraphQLClient, ctx: Context
) -> Generator[CartOperations, None, None]:
    cart_ops = CartOperations(graphql_client)
    _delete_cart_if_exists(cart_ops, ctx)
    yield cart_ops
    _delete_cart_if_exists(cart_ops, ctx)


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@allure.feature("Wishlist / Add and remove products (E2E)")
@allure.title("Add products to a wishlist from grid, list view, and PDP; remove from list")
def test_wishlist_add_from_grid_list_pdp_and_remove(
    page: Page,
    global_settings: GlobalSettings,
    ctx: Context,
    wishlist_ops: ShoppingListOperations,
) -> None:
    wishlist = wishlist_ops.create_shopping_list(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        name=_unique_name("Add products"),
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
        description="Created by wishlist E2E add/remove flow",
    )
    category_page = CategoryPage(
        global_settings=global_settings, page=page, path=_CATEGORY_PATH
    )

    with allure.step("Add a physical product to the wishlist from category grid view"):
        category_page.navigate()
        product_card = category_page.scroll_to_product(_PHYSICAL_PRODUCT_SKU)
        expect(product_card.add_to_list_button).to_be_visible()
        product_card.add_to_list_button.click()
        modal = AddToWishlistsModal(page)
        expect(modal.root).to_be_visible()
        modal.list_checkbox(wishlist.id).click()
        with page.expect_response(_is_wishlist_graphql):
            modal.save_button.click()
        expect(modal.root).not_to_be_visible()
        _wait_for_skus(
            wishlist_ops, wishlist.id, {_PHYSICAL_PRODUCT_SKU}, ctx.culture_name
        )

    with allure.step("Add a product family to the same wishlist from category list view"):
        category_page.view_switcher.list_view_tab.click()
        product_card = category_page.scroll_to_product(_VARIATION_PARENT_SKU)
        expect(product_card.add_to_list_button).to_be_visible()
        product_card.add_to_list_button.click()
        modal = AddToWishlistsModal(page)
        expect(modal.root).to_be_visible()
        modal.list_checkbox(wishlist.id).click()
        with page.expect_response(_is_wishlist_graphql):
            modal.save_button.click()
        expect(modal.root).not_to_be_visible()
        _wait_for_skus(
            wishlist_ops,
            wishlist.id,
            {_PHYSICAL_PRODUCT_SKU, _VARIATION_PARENT_SKU},
            ctx.culture_name,
        )

    with allure.step("Add a variation product to the wishlist from Product Detail Page"):
        product_page = ProductPage(
            global_settings=global_settings, page=page, product_id=_VARIATION_PRODUCT_ID
        )
        product_page.navigate()
        expect(product_page.add_to_list_button).to_be_visible()
        product_page.add_to_list_button.click()
        modal = AddToWishlistsModal(page)
        expect(modal.root).to_be_visible()
        modal.list_checkbox(wishlist.id).click()
        with page.expect_response(_is_wishlist_graphql):
            modal.save_button.click()
        expect(modal.root).not_to_be_visible()
        _wait_for_skus(
            wishlist_ops,
            wishlist.id,
            {_PHYSICAL_PRODUCT_SKU, _VARIATION_PARENT_SKU, _VARIATION_PRODUCT_SKU},
            ctx.culture_name,
        )

    with allure.step("Remove the physical product from the wishlist via the add-to-list modal"):
        category_page.navigate()
        product_card = category_page.scroll_to_product(_PHYSICAL_PRODUCT_SKU)
        product_card.add_to_list_button.click()
        modal = AddToWishlistsModal(page)
        expect(modal.root).to_be_visible()
        modal.list_with_product_checkbox(wishlist.id).click()
        with page.expect_response(_is_wishlist_graphql):
            modal.save_button.click()
        expect(modal.root).not_to_be_visible()
        _wait_for_sku_removed(
            wishlist_ops, wishlist.id, _PHYSICAL_PRODUCT_SKU, ctx.culture_name
        )


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@allure.feature("Wishlist / List management (E2E)")
@allure.title("Create, edit, and remove wishlists with Private, Any, and Organization scopes")
def test_wishlist_create_edit_remove_and_scopes(
    page: Page,
    global_settings: GlobalSettings,
    ctx: Context,
    wishlist_ops: ShoppingListOperations,
) -> None:
    lists_page = AccountListsPage(global_settings=global_settings, page=page)
    lists_page.navigate()

    created: dict[str, str] = {}
    for scope, label in _SCOPE_LABELS.items():
        with allure.step(f"Create wishlist with scope '{scope}'"):
            lists_page.create_list_button.click()
            settings_modal = AddOrUpdateWishlistModal(page)
            expect(settings_modal.root).to_be_visible()
            if settings_modal.sharing_scope_select.count() == 0:
                pytest.skip(
                    "Corporate sharing scope selector is not available for this user"
                )

            name = _unique_name(scope)
            settings_modal.name_input.fill(name)
            settings_modal.description_input.fill(f"{scope} scope created by E2E")
            settings_modal.select_scope(label)
            with page.expect_response(_is_wishlist_graphql):
                settings_modal.save_button.click()
            expect(settings_modal.root).not_to_be_visible()

            card = lists_page.find_card(name)
            expect(card.root).to_be_visible()
            matching = [
                item
                for item in wishlist_ops.get_shopping_lists(
                    store_id=ctx.store_id,
                    user_id=ctx.user_id,
                    currency_code=ctx.currency_code,
                    culture_name=ctx.culture_name,
                )
                if item.name == name
            ]
            assert matching, f"Wishlist '{name}' was not created"
            created[scope] = matching[0].id
            _wait_for_scope(wishlist_ops, matching[0].id, scope, ctx.culture_name)

    original_name = wishlist_ops.get_shopping_list(
        created["Private"], ctx.culture_name
    ).name
    edited_name = _unique_name("Edited")

    with allure.step("Edit wishlist name, description, and scope"):
        card = lists_page.find_card(original_name)
        card.menu_button.click()
        card.edit_menu_item.click()
        settings_modal = AddOrUpdateWishlistModal(page)
        expect(settings_modal.root).to_be_visible()
        settings_modal.name_input.fill(edited_name)
        settings_modal.description_input.fill("Edited by wishlist E2E")
        settings_modal.select_scope(_SCOPE_LABELS["Organization"])
        with page.expect_response(_is_wishlist_graphql):
            settings_modal.save_button.click()
        expect(settings_modal.root).not_to_be_visible()
        expect(lists_page.find_card(edited_name).root).to_be_visible()
        _wait_for_scope(
            wishlist_ops, created["Private"], "Organization", ctx.culture_name
        )

    with allure.step("Delete the edited wishlist"):
        card = lists_page.find_card(edited_name)
        card.menu_button.click()
        card.remove_menu_item.click()
        delete_modal = DeleteWishlistModal(page)
        expect(delete_modal.root).to_be_visible()
        with page.expect_response(_is_wishlist_graphql):
            delete_modal.delete_button.click()
        expect(delete_modal.root).not_to_be_visible()
        expect(card.root).not_to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@allure.feature("Wishlist / Add products to cart (E2E)")
@allure.title("Add all wishlist products to cart from list details")
def test_wishlist_add_all_products_to_cart(
    page: Page,
    global_settings: GlobalSettings,
    ctx: Context,
    clean_cart: CartOperations,
    wishlist_ops: ShoppingListOperations,
) -> None:
    wishlist = wishlist_ops.create_shopping_list(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        name=_unique_name("Cart"),
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
        description="Created by wishlist add-to-cart E2E flow",
    )
    wishlist_ops.add_items_to_shopping_list(
        list_id=wishlist.id,
        items=[
            CartItemInput(product_id=_PHYSICAL_PRODUCT_ID, quantity=1),
            CartItemInput(product_id=_VARIATION_PRODUCT_ID, quantity=1),
        ],
    )
    _wait_for_skus(
        wishlist_ops,
        wishlist.id,
        {_PHYSICAL_PRODUCT_SKU, _VARIATION_PRODUCT_SKU},
        ctx.culture_name,
    )

    with allure.step("Open wishlist details and verify seeded products are shown"):
        details_page = AccountListDetailsPage(
            global_settings=global_settings, page=page, list_id=wishlist.id
        )
        details_page.navigate()
        expect(details_page.line_items).to_have_count(2)
        expect(details_page.find_line_item(_PHYSICAL_PRODUCT_SKU).root).to_be_visible()
        expect(details_page.find_line_item(_VARIATION_PRODUCT_SKU).root).to_be_visible()

    with allure.step("Add all wishlist products to cart and verify cart contents"):
        with page.expect_response(_is_cart_graphql):
            details_page.add_all_to_cart_button.click()
        expect(details_page.cart_quantity_label).to_have_text("2")

        cart_page = CartPage(global_settings=global_settings, page=page)
        cart_page.navigate()
        expect(cart_page.line_items).to_have_count(2)
        expect(cart_page.find_line_item(_PHYSICAL_PRODUCT_SKU).root).to_be_visible()
        expect(cart_page.find_line_item(_VARIATION_PRODUCT_SKU).root).to_be_visible()
