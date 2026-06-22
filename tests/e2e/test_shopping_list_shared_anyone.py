import allure
import pytest
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import ShoppingListOperations
from gql.types import ShoppingList
from playwright.sync_api import Page, expect
from tests.context import Context
from utils.polling_utils import poll_until

_USERNAME = "acme_store_employee_1@acme.com"
_LIST_NAME = "E2E Shared List Anyone"
_LIST_NAME_PRIVATE = "E2E Private List Guard"
_PRODUCT_ID_1 = "smartphone-apple-iphone-17-256gb-black"
_PRODUCT_ID_2 = "smartphone-apple-iphone-17-256gb-mist-blue"
_SCOPE = "AnyoneAnonymous"
_SCOPE_PRIVATE = "Private"


@pytest.mark.e2e
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Wishlist / Shared list (E2E)")
@allure.title("Shared list with AnyoneAnonymous scope is readable by anonymous users")
def test_shopping_list_shared_anyone_read(
    page: Page,
    graphql_client: GraphQLClient,
    global_settings: GlobalSettings,
    ctx: Context,
) -> None:
    ops = ShoppingListOperations(client=graphql_client)
    shopping_list: ShoppingList | None = None

    try:
        with allure.step(f"Create shopping list '{_LIST_NAME}'"):
            shopping_list = ops.create_shopping_list(
                store_id=ctx.store_id,
                user_id=ctx.user_id,
                name=_LIST_NAME,
                currency_code=ctx.currency_code,
                culture_name=ctx.culture_name,
            )
            assert shopping_list.id is not None

        with allure.step(f"Set sharing scope to '{_SCOPE}'"):
            updated = ops.change_shopping_list(
                list_id=shopping_list.id,
                scope=_SCOPE,
            )
            assert updated.sharing_setting is not None
            assert updated.sharing_setting.scope == _SCOPE
            sharing_key = updated.sharing_setting.id

        with allure.step(f"Bulk-add product 1 '{_PRODUCT_ID_1}'"):
            ops.add_bulk_item_to_shopping_list(
                list_id=shopping_list.id,
                product_id=_PRODUCT_ID_1,
            )

        with allure.step(f"Bulk-add product 2 '{_PRODUCT_ID_2}'"):
            ops.add_bulk_item_to_shopping_list(
                list_id=shopping_list.id,
                product_id=_PRODUCT_ID_2,
            )

        with allure.step("Verify list has 2 items (owner view)"):
            seeded = poll_until(
                fetch=lambda: ops.get_shopping_list(list_id=shopping_list.id, culture_name=ctx.culture_name),
                predicate=lambda wl: wl.items_count == 2,
                attempts=global_settings.poll_attempts,
                interval=global_settings.poll_interval,
            )
            assert seeded is not None, "Items did not appear in wishlist after seeding"

        share_url = f"{global_settings.frontend_base_url}/shared-list/{sharing_key}"

        with allure.step(f"Open shared link as anonymous user: {share_url}"):
            browser = page.context.browser
            assert browser is not None, "Playwright browser instance is unavailable"
            anon_context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                ignore_https_errors=True,
            )
            try:
                anon_page = anon_context.new_page()
                anon_page.goto(share_url, wait_until="networkidle")

                with allure.step("Verify both products are visible"):
                    items = anon_page.locator("[data-product-sku]")
                    expect(items).to_have_count(2)

                with allure.step("Verify list is in read-only mode (no add-to-cart controls)"):
                    expect(
                        anon_page.locator("[data-test-id='add-to-cart-component']")
                    ).to_have_count(0)
            finally:
                anon_context.close()

    finally:
        if shopping_list is not None:
            with allure.step(f"Teardown: delete shopping list {shopping_list.id}"):
                ops.delete_shopping_list(list_id=shopping_list.id)


@pytest.mark.e2e
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Wishlist / Shared list (E2E)")
@allure.title("Private list is not accessible by anonymous users via share link")
def test_shopping_list_private_not_accessible_anonymous(
    page: Page,
    graphql_client: GraphQLClient,
    global_settings: GlobalSettings,
    ctx: Context,
) -> None:
    ops = ShoppingListOperations(client=graphql_client)
    shopping_list: ShoppingList | None = None

    try:
        with allure.step(f"Create shopping list '{_LIST_NAME_PRIVATE}' with AnyoneAnonymous scope to obtain sharing key"):
            shopping_list = ops.create_shopping_list(
                store_id=ctx.store_id,
                user_id=ctx.user_id,
                name=_LIST_NAME_PRIVATE,
                currency_code=ctx.currency_code,
                culture_name=ctx.culture_name,
            )
            assert shopping_list.id is not None
            updated = ops.change_shopping_list(list_id=shopping_list.id, scope=_SCOPE)
            assert updated.sharing_setting is not None
            sharing_key = updated.sharing_setting.id

        with allure.step(f"Add product '{_PRODUCT_ID_1}' so list is non-empty"):
            ops.add_bulk_item_to_shopping_list(
                list_id=shopping_list.id,
                product_id=_PRODUCT_ID_1,
            )
            seeded = poll_until(
                fetch=lambda: ops.get_shopping_list(list_id=shopping_list.id, culture_name=ctx.culture_name),
                predicate=lambda wl: wl.items_count == 1,
                attempts=global_settings.poll_attempts,
                interval=global_settings.poll_interval,
            )
            assert seeded is not None, "Item did not appear in wishlist after seeding"

        with allure.step(f"Revoke sharing by changing scope to '{_SCOPE_PRIVATE}'"):
            ops.change_shopping_list(list_id=shopping_list.id, scope=_SCOPE_PRIVATE)
            revoked = poll_until(
                fetch=lambda: ops.get_shopping_list(list_id=shopping_list.id, culture_name=ctx.culture_name),
                predicate=lambda wl: not wl.sharing_setting or wl.sharing_setting.scope == _SCOPE_PRIVATE,
                attempts=global_settings.poll_attempts,
                interval=global_settings.poll_interval,
            )
            assert revoked is not None, "Scope did not revert to Private"

        share_url = f"{global_settings.frontend_base_url}/shared-list/{sharing_key}"

        with allure.step(f"Open previously shared link as anonymous user: {share_url}"):
            browser = page.context.browser
            assert browser is not None, "Playwright browser instance is unavailable"
            anon_context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                ignore_https_errors=True,
            )
            try:
                anon_page = anon_context.new_page()
                anon_page.goto(share_url, wait_until="networkidle")

                with allure.step("Verify no items are accessible (list is private)"):
                    expect(anon_page.locator("[data-product-sku]")).to_have_count(0)
            finally:
                anon_context.close()

    finally:
        if shopping_list is not None:
            with allure.step(f"Teardown: delete shopping list {shopping_list.id}"):
                ops.delete_shopping_list(list_id=shopping_list.id)
