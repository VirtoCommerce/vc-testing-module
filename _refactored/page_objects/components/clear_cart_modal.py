from playwright.sync_api import Locator

from .component import Component


class ClearCartModal(Component):
    @property
    def yes_button(self) -> Locator:
        return self._root.locator("[data-test-id='yes-button']")

    @property
    def no_button(self) -> Locator:
        return self._root.locator("[data-test-id='no-button']")
