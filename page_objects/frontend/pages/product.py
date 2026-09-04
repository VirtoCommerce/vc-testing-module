from playwright.sync_api import Locator, Page

from core.global_settings import GlobalSettings
from page_objects.frontend.components.product_configuration_area import ProductConfigurationArea
from page_objects.frontend.layouts.main import MainLayout


class ProductPage(MainLayout):
    def __init__(
        self,
        global_settings: GlobalSettings,
        page: Page,
        path: str,
    ) -> None:
        super().__init__(global_settings=global_settings, page=page)
        self._path = path

    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/{self._path}"

    @property
    def add_to_list_button(self) -> Locator:
        return self.root.locator("[data-test-id='add-to-list-button']")

    @property
    def product_configuration_area(self) -> ProductConfigurationArea:
        return ProductConfigurationArea(root=self.root.locator(".product-configuration"))

    @property
    def total_price(self) -> Locator:
        return self.root.locator(".product-price__value .price__value")

    @property
    def add_to_cart_button(self) -> Locator:
        return self.root.locator(".product-price__actions button[title='Add to cart']")

    @property
    def update_cart_button(self) -> Locator:
        return self.root.locator(".product-price__actions button[title='Update cart']")

    def add_to_cart(self) -> None:
        self.add_to_cart_button.click()

    def update_cart(self) -> None:
        self.update_cart_button.click()

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")
