from playwright.sync_api import Locator, Page

from fixtures.config import Config
from tests_e2e.pages import CheckoutLayoutPage


class CheckoutReviewOrderPage(CheckoutLayoutPage):
    def __init__(self, config: Config, page: Page):
        self.config = config
        self.page = page

    @property
    def url(self) -> str:
        return f"{self.config['FRONTEND_BASE_URL']}/checkout/review"

    @property
    def place_order_button(self) -> Locator:
        return self.page.locator("[data-test-id='checkout-multi-step.place-order-button']")
