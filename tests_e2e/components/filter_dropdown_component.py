from playwright.sync_api import Locator


class FilterDropdownComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def dropdown_button(self) -> Locator:
        return self.element.locator(".vc-popover__trigger")

    @property
    def dropdown_list(self) -> Locator:
        return self.element.locator(".vc-popover__content")

    def select_item_by_name(self, name: str) -> None:
        self.dropdown_button.click()
        self.dropdown_list.locator(f"[title='{name}']").click()
