from playwright.sync_api import Locator

from page_objects.components.shipping_details_section import ShippingDetailsSection
from page_objects.layouts.checkout import CheckoutLayout


class CheckoutShippingPage(CheckoutLayout):
    _step_path = "shipping"

    @property
    def shipping_details_section(self) -> ShippingDetailsSection:
        return ShippingDetailsSection(root=self._page.locator("[data-test-id='shipping-details-section']"))

    @property
    def billing_button(self) -> Locator:
        return self._page.locator("[data-test-id='billing-button']")
