from playwright.sync_api import Locator
from typing import List, Optional


class CurrencySelectorComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def currency_selector_button(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.top-header.currency-selector-button']")

    @property
    def current_currency_label(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.top-header.current-currency-label']")

    @property
    def currency_selector_menu_items(self) -> List[Locator]:
        return self.element.locator("[data-test-id='main-layout.top-header.currency-selector-item']").all()

    def get_currency_menu_item(self, currency_code: str) -> Optional[Locator]:
        for item in self.currency_selector_menu_items:
            attr = item.get_attribute("data-test-currency-code")
            if attr == currency_code:
                return item
        return None
