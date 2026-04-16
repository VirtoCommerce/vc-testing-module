import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings
from page_objects.components import ClearCartModal
from page_objects.pages import CartPage

_PRODUCT_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"
_QUANTITY = 3


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
def test_cart_clear(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    expect(cart_page.line_items).to_be_visible()
    expect(cart_page.line_items).to_have_count(1)
    expect(cart_page.clear_cart_button).to_be_visible()
    expect(cart_page.clear_cart_button).to_be_enabled()

    cart_page.clear_cart_button.click()
    clear_cart_modal = ClearCartModal(
        root=page.locator("[data-test-id='clear-cart-modal']")
    )
    expect(clear_cart_modal.root).to_be_visible()
    expect(clear_cart_modal.yes_button).to_be_visible()
    expect(clear_cart_modal.yes_button).to_be_enabled()

    clear_cart_modal.yes_button.click()
    expect(clear_cart_modal.root).not_to_be_visible()
    expect(cart_page.line_items).not_to_be_visible()
