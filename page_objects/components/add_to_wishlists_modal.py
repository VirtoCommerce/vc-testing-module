from playwright.sync_api import Locator, Page

from .component import Component


class AddToWishlistsModal(Component):
    def __init__(self, page: Page) -> None:
        super().__init__(
            root=page.locator("[data-test-id='add-to-wishlists-modal']")
        )

    @property
    def save_button(self) -> Locator:
        return self._root.locator("[data-test-id='wishlist-modal-save-button']")

    def list_checkbox(self, list_id: str) -> Locator:
        return self._root.locator(
            f"[data-test-id='wishlist-modal-list-checkbox-{list_id}']"
        )

    def list_with_product_checkbox(self, list_id: str) -> Locator:
        return self._root.locator(
            f"[data-test-id='wishlist-modal-list-with-product-checkbox-{list_id}']"
        )
