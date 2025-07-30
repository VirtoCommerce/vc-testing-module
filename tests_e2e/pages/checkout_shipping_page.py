from playwright.sync_api import Page
from tests_e2e.pages.checkout_layout_page import CheckoutLayoutPage
from tests_e2e.components.checkout_shipping_details_component import CheckoutShippingDetailsComponent
from playwright.sync_api import Locator


class CheckoutShippingPage(CheckoutLayoutPage):
    def __init__(self, config: dict, page: Page):
        self.config = config
        self.page = page

    @property
    def url(self) -> str:
        return f"{self.config['frontend_base_url']}/checkout/shipping"

    @property
    def shipping_details_section_component(self) -> CheckoutShippingDetailsComponent:
        return CheckoutShippingDetailsComponent(self.page.locator("[data-test-id='checkout.shipping-details-section']"))

    @property
    def billing_button(self) -> Locator:
        return self.page.locator("[data-test-id='checkout.billing-button']")
