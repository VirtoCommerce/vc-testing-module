from playwright.sync_api import Locator

from .component import Component


class WishlistCard(Component):
    @property
    def menu_button(self) -> Locator:
        return self._root.locator("[data-test-id='wishlist-card-menu-button']")

    # Menu items are rendered in a portal outside the card root; the :visible
    # filter narrows to the menu of the card that was just opened.
    @property
    def edit_menu_item(self) -> Locator:
        return self._root.page.locator("[data-test-id='wishlist-card-edit-menu-item'] button:visible")

    @property
    def remove_menu_item(self) -> Locator:
        return self._root.page.locator("[data-test-id='wishlist-card-remove-menu-item'] button:visible")
