from playwright.sync_api import Locator

from .component import Component


class AddOrUpdateWishlistModal(Component):
    @property
    def name_input(self) -> Locator:
        return self._root.locator("[data-test-id='wishlist-name-input']")

    @property
    def description_input(self) -> Locator:
        return self._root.locator("[data-test-id='wishlist-description-input'] textarea")

    @property
    def sharing_scope_select(self) -> Locator:
        return self._root.locator("[data-test-id='wishlist-sharing-scope-select']")

    @property
    def save_button(self) -> Locator:
        return self._root.locator("[data-test-id='wishlist-settings-save-button']")

    def select_scope(self, label: str) -> None:
        self.sharing_scope_select.click()
        # The dropdown option is rendered in a portal outside the modal root.
        self._root.page.get_by_role("option", name=label).click()
