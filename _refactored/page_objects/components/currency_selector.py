from playwright.sync_api import Locator

from .component import Component


class CurrencySelector(Component):
    @property
    def button(self) -> Locator:
        return self._root.locator("[data-test-id='currency-selector-button']")

    @property
    def current_currency_label(self) -> Locator:
        return self._root.locator("[data-test-id='current-currency-label']")

    def find_item(self, currency_code: str) -> Locator:
        return self._root.locator(f"[data-currency-code='{currency_code}']")

    def select(self, currency_code: str) -> None:
        self.button.click()
        self.find_item(currency_code=currency_code).click()
