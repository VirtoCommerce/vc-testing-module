from playwright.sync_api import Locator

from page_objects.layouts.main import MainLayout


class AccountCouponsPage(MainLayout):
    """The account promotion-coupons page (``/account/coupons``).

    The coupon UI is class-based in vc-frontend, so locators here use CSS
    classes (``.coupon-item``) rather than ``data-test-id`` attributes.
    """

    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/account/coupons"

    @property
    def cards(self) -> Locator:
        return self._page.locator(".coupon-item")

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")
