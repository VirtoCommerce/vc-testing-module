from playwright.sync_api import Locator

from .component import Component


class QuantityStepper(Component):
    @property
    def increment_button(self) -> Locator:
        return self._root.locator(".vc-quantity-stepper__increment")

    @property
    def decrement_button(self) -> Locator:
        return self._root.locator(".vc-quantity-stepper__decrement")

    @property
    def quantity_input(self) -> Locator:
        return self._root.locator(".vc-input__input")
