from typing import Final

from playwright.sync_api import Locator

from page_objects.backend.page_builder.constants import Column, ListToolbar
from page_objects.backend.shell import Blade, GridRow

_SEARCH_INPUT: Final = ".vc-input input[placeholder='Search...']"
_SEARCH_ENDPOINT: Final = "page-builder-pages/search"
_STATUS_BADGE: Final = ".vc-status__content"


class PageRow(GridRow):
    @property
    def name(self) -> str:
        return self.value(Column.NAME)

    @property
    def permalink(self) -> str:
        return self.value(Column.PERMALINK)

    @property
    def language(self) -> str:
        return self.value(Column.LANGUAGE)

    @property
    def modified_by(self) -> str:
        return self.value(Column.MODIFIED_BY)

    @property
    def modified_date(self) -> str:
        return self.value(Column.MODIFIED)

    @property
    def status_badges(self) -> list[str]:
        return [text.strip() for text in self.cell(Column.STATUS).locator(_STATUS_BADGE).all_inner_texts()]

    @property
    def status(self) -> str:
        badges = self.status_badges
        return badges[0] if badges else ""


class PagesListBlade(Blade):
    @property
    def search_input(self) -> Locator:
        return self._root.locator(_SEARCH_INPUT)

    def wait_for_stable_rows(self, attempts: int = 12, interval_ms: int = 400) -> None:
        page = self._root.page
        previous = self.names
        for _ in range(attempts):
            page.wait_for_timeout(interval_ms)
            current = self.names
            if current == previous:
                return
            previous = current

    def wait_for_total(self, expected: int, attempts: int = 40, interval_ms: int = 200) -> None:
        page = self._root.page
        for _ in range(attempts):
            if self._matches_total(expected):
                return
            page.wait_for_timeout(interval_ms)

    def _matches_total(self, expected: int) -> bool:
        if expected == 0:
            return self.count == 0
        info = self.grid.pagination_info
        if info is None:
            return self.count == expected
        start, end, total = info
        return total == expected and self.count == end - start + 1

    def _apply_search(self, value: str) -> None:
        if self.search_input.input_value() == value:
            return
        page = self._root.page
        with page.expect_response(lambda response: _SEARCH_ENDPOINT in response.url) as response_info:
            self.search_input.fill(value)
        try:
            expected = response_info.value.json().get("totalCount")
        except Exception:  # noqa: BLE001
            expected = None
        if expected is None:
            self.wait_for_stable_rows()
        else:
            self.wait_for_total(int(expected))

    def search(self, term: str) -> None:
        self._apply_search(term)

    def clear_search(self) -> None:
        self._apply_search("")

    def add(self) -> None:
        self.toolbar.click(ListToolbar.ADD)

    def refresh(self) -> None:
        self.toolbar.click(ListToolbar.REFRESH)

    @property
    def names(self) -> list[str]:
        return self.grid.values(Column.NAME)

    @property
    def statuses(self) -> list[str]:
        return self.grid.values(Column.STATUS)

    @property
    def count(self) -> int:
        return self.grid.count

    def row(self, name: str) -> PageRow:
        return PageRow(self.grid.row_locator(Column.NAME, name))

    def open_page(self, name: str) -> None:
        self.reveal(name)
        self.row(name).open()

    def has_page(self, name: str) -> bool:
        return self.grid.row_locator(Column.NAME, name).count() > 0

    def reveal(self, name: str) -> bool:
        if self.has_page(name):
            return True
        self.search(name)
        return self.has_page(name)
