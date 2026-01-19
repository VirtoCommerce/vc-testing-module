import re
from typing import List
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

    @property
    def billing_addresses(self) -> List[Locator]:
        """Get all available billing addresses"""
        return self.page.locator("[data-test-id^='customer-address-']").all()

    @property
    def ok_button(self) -> Locator:
        return self.page.locator("[data-test-id='confirm-button']")

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

    def click_select_billing_address_button(self) -> None:
        """Select billing address on billing page"""
        self.select_billing_address_button.click()

    def select_billing_address_by_index(self, index: int) -> None:
        """Select a billing address by its index (0-based)"""
        addresses = self.billing_addresses
        if index >= len(addresses):
            raise IndexError(f"Address index {index} out of range. Available addresses: {len(addresses)}")
        
        # Get the select button within the specific address row
        address_row = addresses[index]
        # Hover over the address row to ensure it's visible and interactive
        address_row.hover()
        select_button = address_row.get_by_role("button", name="Select")
        select_button.click()
        self.ok_button.click()
        self.requests_tracker.wait_for_all_requests()

    def print_available_billing_addresses(self) -> None:
        """Print all available billing addresses to console"""
        addresses = self.billing_addresses
        print(f"\nAvailable billing addresses: {len(addresses)}")
        for i, address in enumerate(addresses):
            # Get the address text from the second cell
            address_text = address.get_by_role("cell").nth(1).inner_text()
            print(f"  [{i}] {address_text}")

