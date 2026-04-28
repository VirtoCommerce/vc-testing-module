from playwright.sync_api import Locator

from .component import Component


class PaymentDetailsSection(Component):
    @property
    def billing_address_equals_shipping_checkbox(self) -> Locator:
        return self._root.locator(
            '[data-test-id="billing-address-equals-shipping-checkbox"]'
        )

    @property
    def selected_address_label(self) -> Locator:
        return self._root.locator('[data-test-id="selected-address-label"]')

    @property
    def payment_method_selector(self) -> Locator:
        return self._root.locator("[data-test-id='payment-method-selector']")

    def find_selected_payment_method(self, code: str) -> Locator:
        return self._root.locator(f"[data-selected-payment-method-id='{code}']")

    def select_payment_method(self, code: str) -> None:
        self.payment_method_selector.click()
        self._root.locator(f'[data-payment-method-id="{code}"]').click()
