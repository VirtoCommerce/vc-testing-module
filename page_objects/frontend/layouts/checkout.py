from playwright.sync_api import Locator, Page

from core.global_settings import GlobalSettings


class CheckoutLayout:
    _step_path: str

    def __init__(self, global_settings: GlobalSettings, page: Page) -> None:
        self._global_settings = global_settings
        self._page = page

    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/checkout/{self._step_path}"

    @property
    def shipping_cost_label(self) -> Locator:
        return self._page.locator("[data-test-id='shipping-cost-label']")

    def click_outside(self) -> None:
        self._page.locator("body").click()

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")
