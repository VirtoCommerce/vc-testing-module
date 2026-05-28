from playwright.sync_api import Locator

from .component import Component


class DeleteWishlistModal(Component):
    @property
    def delete_button(self) -> Locator:
        return self._root.locator("[data-test-id='delete-button']")
