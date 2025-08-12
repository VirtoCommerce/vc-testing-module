from playwright.sync_api import Locator, Page

from .checkout_layout_page import CheckoutLayoutPage


class CheckoutBillingPage(CheckoutLayoutPage):
    def __init__(self, config: dict, page: Page):
        self.config = config
        self.page = page

    @property
    def url(self) -> str:
        return f"{self.config['frontend_base_url']}/checkout/billing"

    @property
    def payment_method_selector(self) -> Locator:
        return self.page.locator("[data-test-id='checkout.payment-method-selector']")

    @property
    def review_order_button(self) -> Locator:
        return self.page.locator("[data-test-id='checkout.review-order-button']")

    def select_payment_method(self, payment_method: str) -> None:
        self.payment_method_selector.click()
        self.page.locator(f"[data-payment-method-id='{payment_method}']").click()
