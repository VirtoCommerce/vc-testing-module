from playwright.sync_api import Locator

from page_objects.components.line_item import LineItem
from page_objects.layouts.main import MainLayout


class AccountListDetailsPage(MainLayout):
    def __init__(self, list_id: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._list_id = list_id

    @property
    def url(self) -> str:
        return (
            f"{self._global_settings.frontend_base_url}/account/lists/{self._list_id}"
        )

    @property
    def line_items(self) -> Locator:
        return self._page.locator("[data-product-sku]")

    @property
    def add_all_to_cart_button(self) -> Locator:
        return self._page.locator("[data-test-id='add-all-to-cart-button']")

    def find_line_item(self, sku: str) -> LineItem:
        return LineItem(root=self._page.locator(f"[data-product-sku='{sku}']"))

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")
