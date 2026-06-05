from playwright.sync_api import Locator, Page

from core.global_settings import GlobalSettings
from page_objects.layouts.main import MainLayout


class ProductPage(MainLayout):
    def __init__(
        self,
        global_settings: GlobalSettings,
        page: Page,
        product_id: str,
    ) -> None:
        super().__init__(global_settings=global_settings, page=page)
        self._product_id = product_id

    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/product/{self._product_id}"

    @property
    def add_to_list_button(self) -> Locator:
        return self.root.locator("[data-test-id='add-to-list-button']")

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")
