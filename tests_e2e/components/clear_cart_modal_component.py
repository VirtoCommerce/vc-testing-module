from playwright.sync_api import Locator


class ClearCartModalComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def yes_button(self) -> Locator:
        return self.element.locator("[data-test-id='clear-cart-modal.yes-button']")

    @property
    def no_button(self) -> Locator:
        return self.element.locator("[data-test-id='clear-cart-modal.no-button']")
