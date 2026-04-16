from playwright.sync_api import Locator

from page_objects.layouts.main import MainLayout


class CheckoutCompletedPage(MainLayout):
    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/checkout/completed"

    @property
    def created_order_number_label(self) -> Locator:
        return self._page.locator("[data-order-number]")
