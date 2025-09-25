from playwright.sync_api import Locator, Page

from tests_e2e.pages import CheckoutLayoutPage


class CheckoutReviewOrderPage(CheckoutLayoutPage):
    def __init__(self, config: dict, page: Page):
        self.config = config
        self.page = page

    @property
    def url(self) -> str:
        return f"{self.config['frontend_base_url']}/checkout/review"

    @property
    def place_order_button(self) -> Locator:
        return self.page.locator("[data-test-id='checkout.place-order-button']")
