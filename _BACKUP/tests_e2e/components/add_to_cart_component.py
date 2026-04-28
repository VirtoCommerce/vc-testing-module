from playwright.sync_api import Locator


class AddToCartComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def quantity_input(self) -> Locator:
        return self.element.locator("[data-test-id='quantity-input']")

    @property
    def add_to_cart_text_button(self) -> Locator:
        return self.element.locator("[data-test-id='add-to-cart-text-button']")

    @property
    def add_to_cart_icon_button(self) -> Locator:
        return self.element.locator("[data-test-id='add-to-cart-icon-button']")
