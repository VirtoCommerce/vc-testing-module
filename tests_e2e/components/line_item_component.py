from playwright.sync_api import Locator

from .add_to_cart_component import AddToCartComponent
from .quantity_stepper_component import QuantityStepperComponent


class LineItemComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def sku(self) -> str:
        return self.element.get_attribute("data-product-sku")

    @property
    def add_to_cart_component(self) -> AddToCartComponent:
        return AddToCartComponent(
            self.element.locator("[data-test-id='add-to-cart-component']")
        )

    @property
    def quantity_stepper_component(self) -> QuantityStepperComponent:
        return QuantityStepperComponent(
            self.element.locator(".vc-quantity-stepper__input")
        )

    @property
    def remove_button(self) -> Locator:
        return self.element.locator("[data-test-id='remove-item-button']")
