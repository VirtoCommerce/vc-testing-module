from typing import List, Optional

from playwright.sync_api import Locator


class LanguageSelectorComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def language_selector_button(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.top-header.language-selector-button']")

    @property
    def current_language_label(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.top-header.current-language-label']")

    @property
    def language_selector_menu_items(self) -> List[Locator]:
        return self.element.locator("[data-test-id='main-layout.top-header.language-selector-item']").all()

    def get_language_menu_item(self, culture_name: str) -> Optional[Locator]:
        for item in self.language_selector_menu_items:
            attr = item.get_attribute("data-test-culture-name")
            if attr == culture_name:
                return item
        return None
