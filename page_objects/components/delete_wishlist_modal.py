from playwright.sync_api import Locator, Page

from .component import Component


class DeleteWishlistModal(Component):
    def __init__(self, page: Page) -> None:
        super().__init__(root=page.locator("[data-test-id='delete-wishlist-modal']"))

    @property
    def delete_button(self) -> Locator:
        return self._root.locator("[data-test-id='delete-button']")
