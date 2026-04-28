import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import CartPage
from playwright.sync_api import Page, expect

_PRODUCT_ID = "smartphone-samsung-galaxy-a57-5g"
_ORIGINAL_QUANTITY = 3


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _ORIGINAL_QUANTITY)])
def test_cart_item_remove(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()

    line_item = cart_page.find_line_item(sku=_PRODUCT_ID)
    expect(line_item.root).to_be_visible()
    expect(line_item.remove_button).to_be_visible()

    line_item.remove_button.click()
    expect(line_item.root).not_to_be_visible()
