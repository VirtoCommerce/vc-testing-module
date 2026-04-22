from playwright.sync_api import Locator

from page_objects.components.line_item import LineItem
from page_objects.components.payment_details_section import PaymentDetailsSection
from page_objects.components.shipping_details_section import ShippingDetailsSection
from page_objects.layouts.main import MainLayout


class CartPage(MainLayout):
    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/cart"

    @property
    def shipping_details_section(self) -> ShippingDetailsSection:
        return ShippingDetailsSection(root=self._page.locator("[data-test-id='shipping-details-section']"))

    @property
    def payment_details_section(self) -> PaymentDetailsSection:
        return PaymentDetailsSection(root=self._page.locator("[data-test-id='payment-details-section']"))

    @property
    def line_items(self) -> Locator:
        return self._page.locator("[data-product-sku]")

    @property
    def clear_cart_button(self) -> Locator:
        return self._page.locator("[data-test-id='clear-cart-button']")

    @property
    def checkout_button(self) -> Locator:
        return self._page.locator("[data-test-id='checkout-button']")

    @property
    def place_order_button(self) -> Locator:
        return self._page.locator("[data-test-id='place-order-button']")

    @property
    def shipping_cost_label(self) -> Locator:
        return self._page.locator("[data-test-id='shipping-cost-label']")

    def find_line_item(self, sku: str) -> LineItem:
        return LineItem(root=self._page.locator(f"[data-product-sku='{sku}']"))

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")
