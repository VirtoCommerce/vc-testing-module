from typing import Final

from playwright.sync_api import Locator, Page

from page_objects.backend.shell.card import CARD_HEADER, Card
from page_objects.backend.shell.grid import DataGrid
from page_objects.backend.shell.select import SELECT_ROOT, Select
from page_objects.backend.shell.toolbar import BladeToolbar
from page_objects.component import Component

BLADE_ROOT: Final = ".vc-blade"
_TITLE: Final = ".vc-blade-header__title"
_TOOLBAR: Final = "[data-test-id='blade-toolbar']"
_LABEL: Final = ".vc-label"
_FIELD: Final = ".vc-input, .vc-select, .vc-date-picker"
_CARD_TITLE: Final = ".vc-card__title"


class Blade(Component):
    @property
    def title(self) -> Locator:
        return self._root.locator(_TITLE)

    @property
    def toolbar(self) -> BladeToolbar:
        return BladeToolbar(self._root.locator(_TOOLBAR))

    @property
    def grid(self) -> DataGrid:
        return DataGrid(self._root)

    def card(self, title: str) -> Card:
        header = self._root.locator(CARD_HEADER).filter(has_text=title)
        return Card(header.locator("xpath=.."))

    def label(self, text: str) -> Locator:
        return self._root.locator(_LABEL).filter(has_text=text)

    def field(self, label: str) -> Locator:
        return self._root.locator(_FIELD).filter(has=self._root.page.locator(_LABEL, has_text=label))

    def text_input(self, label: str) -> Locator:
        return self.field(label).locator("input").first

    def select(self, label: str) -> Select:
        return Select(self._root.locator(SELECT_ROOT).filter(has=self._root.page.locator(_LABEL, has_text=label)))


class BladeNavigation:
    def __init__(self, page: Page) -> None:
        self._page = page

    @property
    def all(self) -> Locator:
        return self._page.locator(BLADE_ROOT)

    @property
    def count(self) -> int:
        return self.all.count()

    @property
    def first(self) -> Blade:
        return Blade(self.all.first)

    @property
    def last(self) -> Blade:
        return Blade(self.all.last)

    def at(self, index: int) -> Blade:
        return Blade(self.all.nth(index))

    def by_title(self, title: str) -> Blade:
        return Blade(self.all.filter(has=self._page.locator(_TITLE, has_text=title)))
