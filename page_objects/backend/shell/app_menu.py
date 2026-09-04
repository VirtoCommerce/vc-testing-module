from typing import Final

from playwright.sync_api import Locator, Page

_MENU_ITEM: Final = ".vc-menu-item"


class AppMenu:
    def __init__(self, page: Page) -> None:
        self._page = page

    @property
    def items(self) -> Locator:
        return self._page.locator(_MENU_ITEM)

    def item(self, route_id: str) -> Locator:
        return self._page.locator(f"{_MENU_ITEM}[data-test-id='{route_id}']")

    def open(self, route_id: str) -> None:
        self.item(route_id).click()

    @property
    def route_ids(self) -> list[str]:
        return self.items.evaluate_all("nodes => nodes.map(n => n.getAttribute('data-test-id'))")
