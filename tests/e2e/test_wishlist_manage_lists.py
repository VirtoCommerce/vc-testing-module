from uuid import uuid4

import allure
import pytest
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import ShoppingListOperations
from page_objects.pages import AccountListsPage
from playwright.sync_api import Page, Response, expect
from tests.context import Context
from utils.polling_utils import poll_until

_USERNAME = "acme_store_employee_1@acme.com"

_SCOPE_LABELS = {
    "Private": "Private",
    "AnyoneAnonymous": "Anyone (readonly)",
    "Organization": "Organization",
}


def _is_wishlist_manage_mutation(response: Response) -> bool:
    if "/graphql" not in response.url:
        return False
    post = (response.request.post_data or "").lower()
    return "mutation" in post and "wishlist" in post


@pytest.mark.ignore
@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@allure.feature("Wishlist / List management (E2E)")
@allure.title("Create, edit, and remove wishlists with Private, Any, and Organization scopes")
def test_wishlist_create_edit_remove_and_scopes(
    page: Page,
    global_settings: GlobalSettings,
    graphql_client: GraphQLClient,
    ctx: Context,
) -> None:
    ops = ShoppingListOperations(client=graphql_client)
    created_ids: list[str] = []
    lists_page = AccountListsPage(global_settings=global_settings, page=page)
    lists_page.navigate()

    try:
        # Capability check at top of test: corporate sharing scope is only available
        # for users in organizations with sharing enabled. Probe once, then skip if absent.
        lists_page.create_list_button.click()
        probe_modal = lists_page.settings_modal
        expect(probe_modal.root).to_be_visible()
        has_scope_select = probe_modal.sharing_scope_select.count() > 0
        page.keyboard.press("Escape")
        expect(probe_modal.root).not_to_be_visible()
        if not has_scope_select:
            pytest.skip("Corporate sharing scope selector is not available for this user")

        created: dict[str, str] = {}
        for scope, label in _SCOPE_LABELS.items():
            with allure.step(f"Create wishlist with scope '{scope}'"):
                lists_page.create_list_button.click()
                settings_modal = lists_page.settings_modal
                expect(settings_modal.root).to_be_visible()

                name = f"E2E WL {scope[:8]} {uuid4().hex[:6]}"
                settings_modal.name_input.fill(name)
                settings_modal.description_input.fill(f"{scope} scope created by E2E")
                settings_modal.select_scope(label)
                with page.expect_response(_is_wishlist_manage_mutation):
                    settings_modal.save_button.click()
                expect(settings_modal.root).not_to_be_visible()

                card = lists_page.find_card(name)
                expect(card.root).to_be_visible()
                matching = [
                    item
                    for item in ops.get_shopping_lists(
                        store_id=ctx.store_id,
                        user_id=ctx.user_id,
                        currency_code=ctx.currency_code,
                        culture_name=ctx.culture_name,
                    )
                    if item.name == name
                ]
                assert matching, f"Wishlist '{name}' was not created"
                created[scope] = matching[0].id
                created_ids.append(matching[0].id)
                with_scope = poll_until(
                    fetch=lambda lid=matching[0].id: ops.get_shopping_list(list_id=lid, culture_name=ctx.culture_name),
                    predicate=lambda wl, s=scope: (wl.sharing_setting.scope if wl.sharing_setting else None) == s,
                    attempts=global_settings.poll_attempts,
                    interval=global_settings.poll_interval,
                )
                assert with_scope is not None, f"Wishlist {matching[0].id} did not reach scope '{scope}'"

        original_name = ops.get_shopping_list(list_id=created["Private"], culture_name=ctx.culture_name).name
        edited_name = f"E2E WL Edited {uuid4().hex[:6]}"

        with allure.step("Edit wishlist name, description, and scope"):
            card = lists_page.find_card(original_name)
            card.menu_button.click()
            card.edit_menu_item.click()
            settings_modal = lists_page.settings_modal
            expect(settings_modal.root).to_be_visible()
            settings_modal.name_input.fill(edited_name)
            settings_modal.description_input.fill("Edited by wishlist E2E")
            settings_modal.select_scope(_SCOPE_LABELS["Organization"])
            with page.expect_response(_is_wishlist_manage_mutation):
                settings_modal.save_button.click()
            expect(settings_modal.root).not_to_be_visible()
            expect(lists_page.find_card(edited_name).root).to_be_visible()
            edited = poll_until(
                fetch=lambda: ops.get_shopping_list(list_id=created["Private"], culture_name=ctx.culture_name),
                predicate=lambda wl: (wl.sharing_setting.scope if wl.sharing_setting else None) == "Organization",
                attempts=global_settings.poll_attempts,
                interval=global_settings.poll_interval,
            )
            assert edited is not None, "Edited wishlist did not reach Organization scope"

        with allure.step("Delete the edited wishlist"):
            card = lists_page.find_card(edited_name)
            card.menu_button.click()
            card.remove_menu_item.click()
            delete_modal = lists_page.delete_modal
            expect(delete_modal.root).to_be_visible()
            with page.expect_response(_is_wishlist_manage_mutation):
                delete_modal.delete_button.click()
            expect(delete_modal.root).not_to_be_visible()
            expect(card.root).not_to_be_visible()
            created_ids.remove(created["Private"])
    finally:
        for list_id in created_ids:
            try:
                ops.delete_shopping_list(list_id=list_id)
            except Exception as exc:
                allure.attach(
                    f"Teardown of wishlist {list_id} skipped: {exc}",
                    name=f"wishlist-teardown-{list_id}",
                    attachment_type=allure.attachment_type.TEXT,
                )
