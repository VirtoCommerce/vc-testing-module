import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import CartPage
from playwright.sync_api import Page, expect

_PRODUCT_ID = "smartphone-samsung-galaxy-a57-5g"
_ORIGINAL_QUANTITY = 3


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _ORIGINAL_QUANTITY)])
@allure.feature("Cart / Line items (E2E)")
@allure.title("Remove a line item from the cart")
def test_cart_item_remove(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page"):
        cart_page.navigate()

    with allure.step(f"Locate line item for SKU '{_PRODUCT_ID}'"):
        line_item = cart_page.find_line_item(sku=_PRODUCT_ID)
        expect(line_item.root).to_be_visible()
        expect(line_item.remove_button).to_be_visible()

    with allure.step("Click remove and verify the line item disappears"):
        line_item.remove_button.click()
        expect(line_item.root).not_to_be_visible()
