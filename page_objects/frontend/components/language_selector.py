from playwright.sync_api import Locator

from .component import Component


class LanguageSelector(Component):
    @property
    def button(self) -> Locator:
        return self._root.locator("[data-test-id='language-selector-button']")

    @property
    def current_language_label(self) -> Locator:
        return self._root.locator("[data-test-id='current-language-label']")

    def find_item(self, culture_name: str) -> Locator:
        return self._root.locator(f"[data-culture-name='{culture_name}']")

    def select(self, culture_name: str) -> None:
        self.button.click()
        self.find_item(culture_name=culture_name).click()
