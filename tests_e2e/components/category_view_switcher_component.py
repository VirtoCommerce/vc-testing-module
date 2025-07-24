from typing import Literal
from playwright.sync_api import Locator


class CategoryViewSwitcherComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def grid_view_tab(self) -> Locator:
        return self.element.locator("[data-test-id='view-switcher.grid-view-tab']")

    @property
    def list_view_tab(self) -> Locator:
        return self.element.locator("[data-test-id='view-switcher.list-view-tab']")

    def switch_category_view(self, view: Literal["grid", "list"] ) -> None:
        if view == "grid":
            self.grid_view_tab.click()
        elif view == "list":
            self.list_view_tab.click()
