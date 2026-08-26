from datetime import date
from typing import Final

from playwright.sync_api import Locator, expect

from page_objects.component import Component

DATE_PICKER_ROOT: Final = ".vc-date-picker"
_INPUT: Final = "[data-test-id='dp-input']"
_MENU: Final = ".dp__menu"
_NAV_ARROW: Final = ".dp--arrow-btn-nav"
_OUTSIDE: Final = ".vc-blade-header__title"


class DatePicker(Component):
    @property
    def input(self) -> Locator:
        return self._root.locator(_INPUT).first

    @property
    def menu(self) -> Locator:
        return self._root.page.locator(_MENU).first

    @property
    def value(self) -> str:
        return self.input.input_value()

    def day(self, target: date) -> Locator:
        return self._root.page.locator(f"[data-test-id='dp-{target.isoformat()}']")

    def open(self) -> None:
        self.input.click()
        self.menu.wait_for(state="visible")

    def close(self) -> None:
        if not (self.menu.count() and self.menu.is_visible()):
            return
        self._root.page.locator(_OUTSIDE).last.click()
        self.menu.wait_for(state="hidden")

    def select(self, target: date, max_month_steps: int = 12) -> None:
        self.open()
        for _ in range(max_month_steps):
            cell = self.day(target)
            if cell.count() > 0:
                cell.first.click()
                expect(self.input).not_to_have_value("")
                self.close()
                return
            self.menu.locator(_NAV_ARROW).last.click()
        raise AssertionError(f"Date {target.isoformat()} not reachable in the picker")
