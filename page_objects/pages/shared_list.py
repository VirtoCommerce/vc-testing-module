from playwright.sync_api import Locator, Page

from core.global_settings import GlobalSettings
from page_objects.layouts.main import MainLayout


class SharedListPage(MainLayout):
    def __init__(
        self,
        global_settings: GlobalSettings,
        page: Page,
        sharing_key: str,
    ) -> None:
        super().__init__(global_settings=global_settings, page=page)
        self._sharing_key = sharing_key

    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/shared-list/{self._sharing_key}"

    @property
    def list_title(self) -> Locator:
        return self._page.locator(".shared-list__name")

    @property
    def line_items(self) -> Locator:
        return self._page.locator("[data-product-sku]")

    @property
    def add_to_cart_controls(self) -> Locator:
        return self._page.locator("[data-test-id='add-to-cart-component']")

    @property
    def not_found(self) -> Locator:
        # The storefront renders the 404 page when the list is private/not shared.
        return self._page.get_by_role("heading", name="404")

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")
