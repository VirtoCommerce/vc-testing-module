from playwright.sync_api import Locator

from page_objects.layouts.checkout import CheckoutLayout


class CheckoutReviewOrderPage(CheckoutLayout):
    @property
    def line_items(self) -> Locator:
        return self._page.locator("[data-product-sku]")

    @property
    def place_order_button(self) -> Locator:
        return self._page.locator("[data-test-id='place-order-button']")
