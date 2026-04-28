from playwright.sync_api import Locator


class QuantityStepperComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def decrement_button(self) -> Locator:
        return self.element.locator(".vc-quantity-stepper__decrement")

    @property
    def increment_button(self) -> Locator:
        return self.element.locator(".vc-quantity-stepper__increment")

    @property
    def quantity_input(self) -> Locator:
        return self.element.locator(".vc-input__input")
