from playwright.sync_api import Locator

from .add_to_cart_button import AddToCartButton
from .component import Component
from .quantity_stepper import QuantityStepper


class LineItem(Component):
    @property
    def quantity_stepper(self) -> QuantityStepper:
        return QuantityStepper(root=self._root.locator("[data-test-id='quantity-stepper']"))

    @property
    def add_to_cart_button(self) -> AddToCartButton:
        return AddToCartButton(root=self._root.locator("[data-test-id='add-to-cart-button']"))

    @property
    def remove_button(self) -> Locator:
        return self._root.locator("[data-test-id='remove-item-button']")

    @property
    def save_for_later_desktop_button(self) -> Locator:
        return self._root.locator(
            "[data-test-id='cart-item-actions-after-title'] [data-test-id='save-for-later-button']"
        )
