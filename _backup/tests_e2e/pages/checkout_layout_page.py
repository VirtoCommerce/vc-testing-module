from playwright.sync_api import Locator, Page

from tests_e2e.components import OrderSummaryComponent


class CheckoutLayoutPage:
    def __init__(self, page: Page):
        self.page = page

    @property
    def secure_checkout_label(self) -> Locator:
        return self.page.locator("[data-test-id='checkout-layout.secure-checkout-label']")

    @property
    def order_summary_component(self) -> OrderSummaryComponent:
        return OrderSummaryComponent(self.page.locator("[data-test-id='order-summary-widget']"))
