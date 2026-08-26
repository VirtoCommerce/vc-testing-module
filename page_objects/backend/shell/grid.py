import re
from typing import Final

from playwright.sync_api import Locator

from page_objects.component import Component

_DATA_ROW: Final = "[role='row']:has([role='cell'])"
_HEADER_ROW: Final = "[role='row']:has([role='columnheader'])"
_EMPTY_STATE: Final = ".vc-table-composition__empty-state"
_PAGINATION: Final = ".vc-data-table__pagination"
_RANGE_PATTERN: Final = re.compile(r"(\d+)\s*\D\s*(\d+)\s+of\s+(\d+)")
_SELECTION_CELL: Final = ".vc-data-table__selection-cell"
_SELECTION_CHECKBOX: Final = f"{_SELECTION_CELL} input[type='checkbox']"
_SELECTION_CONTROL: Final = f"{_SELECTION_CELL} .vc-checkbox__container"


class GridRow(Component):
    def cell(self, column_id: str) -> Locator:
        return self._root.locator(f"[data-column-id='{column_id}']")

    def value(self, column_id: str) -> str:
        return (self.cell(column_id).inner_text() or "").strip()

    @property
    def checkbox(self) -> Locator:
        return self._root.locator(_SELECTION_CHECKBOX)

    @property
    def selection_control(self) -> Locator:
        return self._root.locator(_SELECTION_CONTROL)

    @property
    def is_selected(self) -> bool:
        return self.checkbox.is_checked()

    def select(self) -> None:
        if not self.is_selected:
            self.selection_control.click()

    def deselect(self) -> None:
        if self.is_selected:
            self.selection_control.click()

    def open(self) -> None:
        self._root.click()


class DataGrid(Component):
    @property
    def rows(self) -> Locator:
        return self._root.locator(_DATA_ROW)

    @property
    def header(self) -> Locator:
        return self._root.locator(_HEADER_ROW)

    @property
    def empty_state(self) -> Locator:
        return self._root.locator(_EMPTY_STATE)

    @property
    def count(self) -> int:
        return self.rows.count()

    @property
    def total_count(self) -> int:
        info = self.pagination_info
        return info[2] if info else self.count

    @property
    def pagination_info(self) -> tuple[int, int, int] | None:
        label = self._root.locator(_PAGINATION)
        if label.count() == 0:
            return None
        match = _RANGE_PATTERN.search(label.first.inner_text() or "")
        if not match:
            return None
        return int(match.group(1)), int(match.group(2)), int(match.group(3))

    def column_header(self, column_id: str) -> Locator:
        return self.header.locator(f"[data-column-id='{column_id}']")

    def row(self, index: int) -> GridRow:
        return GridRow(self.rows.nth(index))

    def row_locator(self, column_id: str, value: str, exact: bool = True) -> Locator:
        text: str | re.Pattern[str] = re.compile(rf"^\s*{re.escape(value)}\s*$") if exact else value
        cell = self._root.page.locator(f"[data-column-id='{column_id}']")
        return self.rows.filter(has=cell.filter(has_text=text))

    def row_by(self, column_id: str, value: str, exact: bool = True) -> GridRow:
        return GridRow(self.row_locator(column_id, value, exact))

    def values(self, column_id: str) -> list[str]:
        return [(text or "").strip() for text in self.rows.locator(f"[data-column-id='{column_id}']").all_inner_texts()]
