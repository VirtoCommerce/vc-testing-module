import re
from playwright.sync_api import Locator, Page

from .checkout_layout_page import CheckoutLayoutPage
from fixtures.requests_tracker import RequestsTracker


class CheckoutBillingPage(CheckoutLayoutPage):
    def __init__(self, config: dict, page: Page, requests_tracker: RequestsTracker):
        self.config = config
        self.page = page
        self.requests_tracker = requests_tracker
            
    @property
    def url(self) -> str:
        return f"{self.config['frontend_base_url']}/checkout/billing"

    @property
    def payment_method_selector(self) -> Locator:
        # Select the payment method dropdown/trigger by its visible text
        return self.page.get_by_text("Select a payment method")

    @property
    def review_order_button(self) -> Locator:
        return self.page.locator("[data-test-id='checkout.review-order-button']")

    @property
    def select_billing_address_button(self) -> Locator:
        return self.page.locator("[data-test-id='select-address-button']")

    def select_purchase_order_payment_method(self) -> None:
        self.payment_method_selector.click()
        self.page.locator("[data-payment-method-id='PurchaseOrderPaymentMethod']").wait_for(state="visible", timeout=30000)
        self.page.locator("[data-payment-method-id='PurchaseOrderPaymentMethod']").click()

    def select_card_payment_method(self) -> None:
        """Select card payment method on billing page"""
        self.payment_method_selector.click()
        self.page.locator("[data-payment-method-id='SkyflowPaymentMethod']").wait_for(state="visible", timeout=30000)
        self.page.locator("[data-payment-method-id='SkyflowPaymentMethod']").click()
        self.requests_tracker.wait_for_all_requests()

    def select_billing_address(self) -> None:
        """Select billing address on billing page"""
        self.select_billing_address_button.click()
