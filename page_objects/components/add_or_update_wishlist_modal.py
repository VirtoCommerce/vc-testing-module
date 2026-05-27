from playwright.sync_api import Locator, Page

from .component import Component


class AddOrUpdateWishlistModal(Component):
    def __init__(self, page: Page) -> None:
        super().__init__(
            root=page.locator("[data-test-id='add-or-update-wishlist-modal']")
        )

    @property
    def name_input(self) -> Locator:
        return self._root.locator("[data-test-id='wishlist-name-input']")

    @property
    def description_input(self) -> Locator:
        return self._root.locator(
            "[data-test-id='wishlist-description-input'] textarea"
        )

    @property
    def sharing_scope_select(self) -> Locator:
        return self._root.locator("[data-test-id='wishlist-sharing-scope-select']")

    @property
    def save_button(self) -> Locator:
        return self._root.locator("[data-test-id='wishlist-settings-save-button']")

    def select_scope(self, label: str) -> None:
        self.sharing_scope_select.click()
        self._root.page.get_by_role("option", name=label).click()
