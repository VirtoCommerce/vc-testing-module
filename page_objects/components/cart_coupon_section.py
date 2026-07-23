import re

from playwright.sync_api import Locator

from .component import Component


class CartCouponSection(Component):

    @property
    def preset_cards(self) -> Locator:
        return self._root.locator(".coupon-card:has(input[readonly])")

    def first_preset_code(self) -> str:
        aria = self.preset_cards.first.get_by_role("button").first.get_attribute("aria-label") or ""
        match = re.search(r"Apply coupon\s+(.+)$", aria, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def apply_preset(self, code: str) -> None:
        self._root.get_by_role(
            "button", name=re.compile(rf"Apply coupon\s+{re.escape(code)}\b", re.IGNORECASE)
        ).first.click()

    @property
    def custom_code_card(self) -> Locator:
        return self._root.locator(".coupon-card:has(input:not([readonly]))")

    @property
    def custom_code_input(self) -> Locator:
        return self.custom_code_card.locator("input").first

    @property
    def apply_button(self) -> Locator:
        return self.custom_code_card.get_by_role("button").first

    @property
    def applied_cards(self) -> Locator:
        return self._root.locator(".coupon-card--applied")

    @property
    def applied_code_input(self) -> Locator:
        """Readonly code field of the currently applied preset card.

        The code field keeps its value in both the default and applied
        states, so the applied coupon is identified by its code rather than
        by the promotion's display name (which the applied card's button
        drops, and whose text is edit-prone). Pair with ``expect(...)
        .to_have_value(code)`` so the assertion polls out the non-atomic
        switch between two applied coupons.
        """
        return self.applied_cards.first.locator("input[readonly]").first

    @property
    def applied_check_icon(self) -> Locator:
        return self._root.locator(".coupon-card--applied .lucide-circle-check")

    @property
    def view_all_link(self) -> Locator:
        return self._root.locator(".coupons-section__link")

    @property
    def remove_button(self) -> Locator:
        return self._root.get_by_role("button", name=re.compile("remove coupon", re.IGNORECASE)).first

    @property
    def error_message(self) -> Locator:
        return self._root.locator(".coupon-card__error, [role='alert']").first
