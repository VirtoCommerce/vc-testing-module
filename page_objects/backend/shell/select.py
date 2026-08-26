import re
from typing import Final

from playwright.sync_api import Locator, expect

from page_objects.component import Component

SELECT_ROOT: Final = ".vc-select"
_TOGGLE: Final = "[data-test-id='dropdown-toggle']"
_DROPDOWN: Final = "[data-test-id='dropdown']"
_OPTION: Final = "[data-test-id='option']"
_TRANSITION_PATTERN: Final = re.compile(r"select-dropdown-(enter|leave)-active")


class Select(Component):
    @property
    def toggle(self) -> Locator:
        return self._root.locator(_TOGGLE)

    @property
    def value(self) -> str:
        return (self.toggle.inner_text() or "").strip()

    @property
    def options(self) -> Locator:
        return self._root.page.locator(_OPTION)

    @property
    def dropdown(self) -> Locator:
        return self._root.page.locator(_DROPDOWN).first

    def open(self) -> Locator:
        self.toggle.click()
        self.dropdown.wait_for(state="visible")
        expect(self.dropdown).not_to_have_class(_TRANSITION_PATTERN)
        return self.options

    def close(self) -> None:
        self._root.page.keyboard.press("Escape")
        self.dropdown.wait_for(state="hidden")

    def option_texts(self) -> list[str]:
        self.open()
        texts = [text.strip() for text in self.options.all_inner_texts()]
        self.close()
        return texts

    def select(self, option: str) -> None:
        self.open()
        self.options.filter(has_text=re.compile(rf"^\s*{re.escape(option)}\s*$")).first.click()
