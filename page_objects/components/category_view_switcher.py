from playwright.sync_api import Locator

from .component import Component


class CategoryViewSwitcher(Component):
    @property
    def grid_view_tab(self) -> Locator:
        return self._root.locator("[data-test-id='grid-view-tab']")

    @property
    def list_view_tab(self) -> Locator:
        return self._root.locator("[data-test-id='list-view-tab']")
