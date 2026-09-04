from typing import Final

from playwright.sync_api import Locator, expect

from page_objects.component import Component

CARD_ROOT: Final = ".vc-card"
CARD_HEADER: Final = ".vc-card__header"
_HEADER: Final = "> .vc-card__header"
_TITLE: Final = "> .vc-card__header .vc-card__title"
_BODY: Final = "> .vc-card__body"
_COLLAPSABLE: Final = "vc-card--collapsable"


class Card(Component):
    @property
    def header(self) -> Locator:
        return self._root.locator(_HEADER).first

    @property
    def title(self) -> Locator:
        return self._root.locator(_TITLE).first

    @property
    def body(self) -> Locator:
        return self._root.locator(_BODY).first

    @property
    def is_collapsible(self) -> bool:
        return _COLLAPSABLE in (self._root.get_attribute("class") or "").split()

    @property
    def is_expanded(self) -> bool:
        if not self.is_collapsible:
            return True
        return self.header.get_attribute("aria-expanded") == "true"

    def expand(self) -> "Card":
        if self.is_collapsible and not self.is_expanded:
            self.header.click()
            expect(self.header).to_have_attribute("aria-expanded", "true")
        return self

    def collapse(self) -> "Card":
        if self.is_collapsible and self.is_expanded:
            self.header.click()
            expect(self.header).to_have_attribute("aria-expanded", "false")
        return self
