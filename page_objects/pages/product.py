from playwright.sync_api import Locator

from page_objects.layouts.main import MainLayout


class ProductPage(MainLayout):
    def __init__(self, product_id: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._product_id = product_id

    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/product/{self._product_id}"

    @property
    def add_to_list_button(self) -> Locator:
        return self._page.locator("[data-test-id='add-to-list-button']").first

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")

