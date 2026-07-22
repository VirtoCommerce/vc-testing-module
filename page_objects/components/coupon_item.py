from playwright.sync_api import Locator

from .component import Component


class CouponItem(Component):
    """A single promotion-coupon card (``.coupon-item``).

    Rendered on the account coupons page and, in themes that surface preset
    coupons, inside the cart coupon section. The coupon UI is class-based in
    vc-frontend, so locators here use the ``coupon-item__*`` BEM classes rather
    than ``data-test-id`` attributes.
    """

    @property
    def code_button(self) -> Locator:
        return self._root.locator(".coupon-item__code-button")

    @property
    def code_value(self) -> Locator:
        return self._root.locator(".coupon-item__code-value")

    def code(self) -> str:
        return self.code_value.inner_text().strip()
