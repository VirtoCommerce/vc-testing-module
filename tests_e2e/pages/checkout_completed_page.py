from playwright.sync_api import Page

from .main_layout_page import MainLayoutPage


class CheckoutCompletedPage(MainLayoutPage):
    def __init__(self, config: dict, page: Page):
        self.config = config
        self.page = page

    @property
    def url(self) -> str:
        return f"{self.config['frontend_base_url']}/checkout/completed"

    @property
    def order_number(self) -> str:
        return self.page.locator("[data-order-number]").get_attribute(
            "data-order-number"
        )
