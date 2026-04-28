from playwright.sync_api import Locator, Page

from core.global_settings import GlobalSettings
from page_objects.components.top_header import TopHeader


class MainLayout:
    def __init__(self, page: Page, global_settings: GlobalSettings) -> None:
        self._global_settings = global_settings
        self._page = page

    @property
    def root(self) -> Locator:
        return self._page.locator(".main-layout")

    @property
    def top_header(self) -> TopHeader:
        return TopHeader(root=self._page.locator("[data-test-id='top-header']"))

    @property
    def cart_quantity_label(self) -> Locator:
        return self._page.locator(
            "[data-test-id='desktop-main-menu-cart-link'] .vc-badge__content"
        )

    def click_outside(self) -> None:
        self._page.locator("body").click()
