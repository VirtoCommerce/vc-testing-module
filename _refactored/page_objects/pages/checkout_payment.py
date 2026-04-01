from playwright.sync_api import Locator

from page_objects.components.payment_details_section import PaymentDetailsSection
from page_objects.layouts.checkout import CheckoutLayout


class CheckoutPaymentPage(CheckoutLayout):
    _step_path = "billing"

    @property
    def payment_details_section(self) -> PaymentDetailsSection:
        return PaymentDetailsSection(
            root=self._page.locator("[data-test-id='payment-details-section']")
        )

    @property
    def review_order_button(self) -> Locator:
        return self._page.locator("[data-test-id='review-order-button']")
