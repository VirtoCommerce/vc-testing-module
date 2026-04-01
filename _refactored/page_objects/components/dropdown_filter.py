from playwright.sync_api import Locator

from .component import Component


class DropdownFilter(Component):
    @property
    def dropdown_button(self) -> Locator:
        return self._root.locator(".vc-popover__trigger")

    @property
    def dropdown_list(self) -> Locator:
        return self._root.locator(".vc-popover__content")

    def select_item_by_name(self, name: str) -> None:
        self.dropdown_button.click()
        self.dropdown_list.locator(f"[title='{name}']").click()
