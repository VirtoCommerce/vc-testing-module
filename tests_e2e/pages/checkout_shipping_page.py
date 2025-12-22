from playwright.sync_api import Locator, Page

from fixtures.config import Config
from tests_e2e.components import CheckoutShippingDetailsComponent
from tests_e2e.pages import CheckoutLayoutPage


class CheckoutShippingPage(CheckoutLayoutPage):
    def __init__(self, config: Config, page: Page):
        self.config = config
        self.page = page

    @property
    def url(self) -> str:
        return f"{self.config['FRONTEND_BASE_URL']}/checkout/shipping"

    @property
    def shipping_details_section_component(self) -> CheckoutShippingDetailsComponent:
        return CheckoutShippingDetailsComponent(
            self.page.locator("[data-test-id='checkout.shipping-details-section']")
        )

    @property
    def billing_button(self) -> Locator:
        return self.page.locator("[data-test-id='checkout.billing-button']")
