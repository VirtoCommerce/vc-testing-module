from playwright.sync_api import Locator


class DeleteWishlistProductModalComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def delete_button(self) -> Locator:
        return self.element.locator("[data-test-id='delete-wishlist-product-modal.delete-button']")

    @property
    def cancel_button(self) -> Locator:
        return self.element.locator("[data-test-id='delete-wishlist-product-modal.cancel-button']")
