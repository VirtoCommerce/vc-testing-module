from .add_to_cart_button import AddToCartButton
from .component import Component
from .quantity_stepper import QuantityStepper


class LineItem(Component):
    @property
    def quantity_stepper(self) -> QuantityStepper:
        return QuantityStepper(
            root=self._root.locator("[data-test-id='quantity-stepper']")
        )

    @property
    def add_to_cart_button(self) -> AddToCartButton:
        return AddToCartButton(
            root=self._root.locator("[data-test-id='add-to-cart-button']")
        )
