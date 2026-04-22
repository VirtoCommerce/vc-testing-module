from typing import List, Optional

from playwright.sync_api import Page

from fixtures.config import Config
from tests_e2e.components import LineItemComponent
from tests_e2e.components.delete_wishlist_product_modal import (
    DeleteWishlistProductModalComponent,
)

from .main_layout_page import MainLayoutPage


class SaveForLaterPage(MainLayoutPage):
    def __init__(self, page: Page, config: Config):
        self.page = page
        self.config = config

    @property
    def url(self) -> str:
        return f"{self.config['FRONTEND_BASE_URL']}/account/saved-for-later"

    @property
    def line_items(self) -> List[LineItemComponent]:
        return [LineItemComponent(item) for item in self.page.locator("[data-test-id='line-item']").all()]

    @property
    def is_empty(self) -> bool:
        return len(self.line_items) == 0

    def navigate(self):
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    def get_line_item_by_sku(self, sku: str) -> Optional[LineItemComponent]:
        for line_item in self.line_items:
            if line_item.sku == sku:
                return line_item
        return None

    def remove_line_item(self, sku: str) -> None:
        line_item = self.get_line_item_by_sku(sku)
        if line_item:
            line_item.remove_button.click()
            modal = DeleteWishlistProductModalComponent(
                self.page.locator("[data-test-id='delete-wishlist-product-modal']")
            )
            modal.delete_button.click()
        self.page.wait_for_load_state("networkidle")
