from playwright.sync_api import Page

from fixtures.config import Config

from .main_layout_page import MainLayoutPage


class CheckoutCompletedPage(MainLayoutPage):
    def __init__(self, config: Config, page: Page):
        self.config = config
        self.page = page

    @property
    def url(self) -> str:
        return f"{self.config['FRONTEND_BASE_URL']}/checkout/completed"

    @property
    def order_number(self) -> str:
        return self.page.locator("[data-order-number]").get_attribute("data-order-number")
