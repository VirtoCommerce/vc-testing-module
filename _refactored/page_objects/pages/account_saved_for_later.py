from page_objects.components.line_item import LineItem
from page_objects.layouts.main import MainLayout
from playwright.sync_api import Locator


class AccountSavedForLaterPage(MainLayout):
    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/account/saved-for-later"

    @property
    def line_items(self) -> Locator:
        return self._page.locator("[data-product-sku]")

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")

    def find_line_item(self, sku: str) -> LineItem:
        return LineItem(root=self._page.locator(f"[data-product-sku='{sku}']"))
