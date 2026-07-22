import re

from playwright.sync_api import Locator

from .component import Component


class CartCouponSection(Component):
    """The cart/checkout coupon area (``.coupons-section``).

    Surfaces the manual promotion-code input plus (in themes that support it)
    a set of preset coupon cards discovered from the ``promotionCoupons`` query.
    The coupon UI is class-based in vc-frontend, so locators here use CSS
    classes and accessible roles rather than ``data-test-id`` attributes.

    Preset coupon cards may only exist in the PR/preview theme, so callers
    should probe ``root`` / ``preset_cards`` and skip when the feature is
    absent rather than assume it is present.
    """

    @property
    def preset_cards(self) -> Locator:
        return self._root.locator(".coupon-item")

    def first_preset_code(self) -> str:
        return self.preset_cards.first.locator(".coupon-item__code-value").inner_text().strip()

    def apply_preset(self, code: str) -> None:
        # TODO(VCST-4776): the preset "apply" control selector is unverified
        # against the PR/preview theme. It must NOT be ``.coupon-item__code-button``
        # — that class copies the code to the clipboard on the account page. We
        # target a dedicated apply/add/use button scoped to the preset card so a
        # wrong selector fails loudly (no match) rather than silently copying.
        card = self.preset_cards.filter(has_text=code).first
        card.get_by_role("button", name=re.compile(r"apply|add|use", re.IGNORECASE)).first.click()

    @property
    def custom_code_input(self) -> Locator:
        return self._root.locator("input").first

    @property
    def apply_button(self) -> Locator:
        by_name = self._root.get_by_role("button", name=re.compile("apply", re.IGNORECASE))
        # Class-based fallback for icon-only / non-labelled apply controls.
        by_class = self._root.locator(".coupons-section__apply-button, [data-test-id='apply-coupon-button']")
        return by_name.or_(by_class).first

    @property
    def remove_button(self) -> Locator:
        by_name = self._root.get_by_role("button", name=re.compile("remove", re.IGNORECASE))
        # Class-based fallback: removal may be an icon-only "×" with no text/name.
        by_class = self._root.locator(".coupons-section__remove-button, [data-test-id='remove-coupon-button']")
        return by_name.or_(by_class).first
