from playwright.sync_api import Locator

from .component import Component


class RemoveShoppingListItemModal(Component):
    @property
    def delete_button(self) -> Locator:
        return self._root.locator("[data-test-id='delete-button']")

    @property
    def cancel_button(self) -> Locator:
        return self._root.locator("[data-test-id='cancel-button']")
