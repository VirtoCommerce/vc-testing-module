from playwright.sync_api import Locator, Page

from fixtures.config import Config
from tests_e2e.components import CheckoutPaymentDetailsComponent

from .checkout_layout_page import CheckoutLayoutPage


class CheckoutBillingPage(CheckoutLayoutPage):
    def __init__(self, config: Config, page: Page):
        self.config = config
        self.page = page

    @property
    def url(self) -> str:
        return f"{self.config['FRONTEND_BASE_URL']}/checkout/billing"

    @property
    def payment_details_section_component(self) -> CheckoutPaymentDetailsComponent:
        return CheckoutPaymentDetailsComponent(self.page.locator("[data-test-id='checkout.payment-details-section']"))

    @property
    def review_order_button(self) -> Locator:
        return self.page.locator("[data-test-id='checkout.review-order-button']")
