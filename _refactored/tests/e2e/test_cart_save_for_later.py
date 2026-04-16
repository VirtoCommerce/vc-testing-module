import pytest
from core.global_settings import GlobalSettings
from page_objects.components import RemoveShoppingListItemModal
from page_objects.pages import AccountSavedForLaterPage, CartPage
from playwright.sync_api import Page, expect

_PRODUCT_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"
_ORIGINAL_QUANTITY = 3
_USERNAME = "acme_store_employee_1@acme.com"


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _ORIGINAL_QUANTITY)])
@pytest.mark.quantity_control("stepper")
def test_cart_save_for_later(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()

    line_item = cart_page.find_line_item(sku=_PRODUCT_ID)
    expect(line_item.root).to_be_visible()
    expect(line_item.save_for_later_desktop_button).to_be_visible()

    line_item.save_for_later_desktop_button.click()
    line_item.wait_for_results()
    expect(cart_page.line_items).to_have_count(0)

    account_saved_for_later_page = AccountSavedForLaterPage(
        global_settings=global_settings, page=page
    )
    account_saved_for_later_page.navigate()
    expect(account_saved_for_later_page.line_items).to_have_count(1)

    saved_item = account_saved_for_later_page.find_line_item(sku=_PRODUCT_ID)
    expect(saved_item.root).to_be_visible()

    saved_item.remove_button.click()

    remove_item_modal = RemoveShoppingListItemModal(
        root=page.locator("[data-test-id='delete-wishlist-product-modal']")
    )
    expect(remove_item_modal.root).to_be_visible()

    remove_item_modal.delete_button.click()
    expect(saved_item.root).not_to_be_visible()
