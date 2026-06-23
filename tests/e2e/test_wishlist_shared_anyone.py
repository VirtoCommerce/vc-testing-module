import allure
import pytest
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import ShoppingListOperations
from gql.types import ShoppingList
from page_objects.pages import SharedListPage
from playwright.sync_api import Browser, BrowserContext, expect
from tests.context import Context
from utils.polling_utils import poll_until

_USERNAME = "acme_store_employee_1@acme.com"
_LIST_NAME = "E2E Shared List Anyone"
_LIST_NAME_PRIVATE = "E2E Private List Guard"
_PRODUCT_ID_1 = "smartphone-apple-iphone-17-256gb-black"
_PRODUCT_ID_2 = "smartphone-apple-iphone-17-256gb-mist-blue"
_SCOPE = "AnyoneAnonymous"
_SCOPE_PRIVATE = "Private"
_VIEWPORT = {"width": 1920, "height": 1080}


def _anonymous_context(browser: Browser) -> BrowserContext:
    # Fresh, unauthenticated context so the share link is opened as a guest.
    return browser.new_context(viewport=_VIEWPORT)


def _wait_for_items_count(
    ops: ShoppingListOperations,
    list_id: str,
    culture_name: str,
    expected: int,
    global_settings: GlobalSettings,
) -> ShoppingList | None:
    return poll_until(
        fetch=lambda: ops.get_shopping_list(list_id=list_id, culture_name=culture_name),
        predicate=lambda wl: wl.items_count == expected,
        attempts=global_settings.poll_attempts,
        interval=global_settings.poll_interval,
    )


@pytest.mark.e2e
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Wishlist / Shared list (E2E)")
@allure.title("Shared list with AnyoneAnonymous scope is readable by anonymous users")
def test_wishlist_shared_anyone_read(
    browser: Browser,
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

        for product_id in (_PRODUCT_ID_1, _PRODUCT_ID_2):
            with allure.step(f"Bulk-add product '{product_id}'"):
                ops.add_bulk_item_to_shopping_list(
                    list_id=shopping_list.id,
                    product_id=product_id,
                )

        with allure.step("Verify list has 2 items (owner view)"):
            seeded = _wait_for_items_count(ops, shopping_list.id, ctx.culture_name, 2, global_settings)
            assert seeded is not None, "Items did not appear in wishlist after seeding"

        with allure.step("Open shared link as anonymous user"):
            context = _anonymous_context(browser)
            try:
                shared = SharedListPage(
                    global_settings=global_settings,
                    page=context.new_page(),
                    sharing_key=sharing_key,
                )
                shared.navigate()

                with allure.step("Verify the shared list renders with its name and both products"):
                    expect(shared.list_title).to_have_text(_LIST_NAME)
                    expect(shared.line_items).to_have_count(2)

                with allure.step("Verify list is read-only (no add-to-cart controls)"):
                    expect(shared.add_to_cart_controls).to_have_count(0)
            finally:
                context.close()

    finally:
        if shopping_list is not None:
            with allure.step(f"Teardown: delete shopping list {shopping_list.id}"):
                ops.delete_shopping_list(list_id=shopping_list.id)


@pytest.mark.e2e
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Wishlist / Shared list (E2E)")
@allure.title("Private list is not accessible by anonymous users via share link")
def test_wishlist_private_not_accessible_anonymous(
    browser: Browser,
    graphql_client: GraphQLClient,
    global_settings: GlobalSettings,
    ctx: Context,
) -> None:
    ops = ShoppingListOperations(client=graphql_client)
    shopping_list: ShoppingList | None = None

    try:
        with allure.step(f"Create shopping list '{_LIST_NAME_PRIVATE}' with '{_SCOPE}' scope to obtain a sharing key"):
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
            seeded = _wait_for_items_count(ops, shopping_list.id, ctx.culture_name, 1, global_settings)
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

        with allure.step("Open previously shared link as anonymous user"):
            context = _anonymous_context(browser)
            try:
                shared = SharedListPage(
                    global_settings=global_settings,
                    page=context.new_page(),
                    sharing_key=sharing_key,
                )
                shared.navigate()

                with allure.step("Verify access is blocked: not-found page shown, no list content"):
                    expect(shared.not_found).to_be_visible()
                    expect(shared.list_title).to_have_count(0)
                    expect(shared.line_items).to_have_count(0)
            finally:
                context.close()

    finally:
        if shopping_list is not None:
            with allure.step(f"Teardown: delete shopping list {shopping_list.id}"):
                ops.delete_shopping_list(list_id=shopping_list.id)


@pytest.mark.e2e
@pytest.mark.optional
@allure.feature("Wishlist / Shared list (E2E)")
@allure.title("Malformed sharing key shows the not-found page for anonymous users")
def test_wishlist_shared_invalid_key(
    browser: Browser,
    global_settings: GlobalSettings,
) -> None:
    context = _anonymous_context(browser)
    try:
        shared = SharedListPage(
            global_settings=global_settings,
            page=context.new_page(),
            sharing_key="non-existent-sharing-key-000000",
        )

        with allure.step("Open a shared link with an invalid key as anonymous user"):
            shared.navigate()

        with allure.step("Verify not-found page is shown and no list content renders"):
            expect(shared.not_found).to_be_visible()
            expect(shared.line_items).to_have_count(0)
    finally:
        context.close()
