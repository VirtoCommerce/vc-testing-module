from playwright.sync_api import Locator

from .component import Component


class AddToCartButton(Component):
    @property
    def quantity_input(self) -> Locator:
        return self._root.locator(".vc-input__input")

    @property
    def text_button(self) -> Locator:
        return self._root.locator(".vc-add-to-cart__text-button")

    @property
    def icon_button(self) -> Locator:
        return self._root.locator(".vc-add-to-cart__icon-button")
