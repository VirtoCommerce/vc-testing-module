from playwright.sync_api import Locator

from .add_to_cart_button import AddToCartButton
from .component import Component
from .line_item import LineItem
from .quantity_stepper import QuantityStepper


class ProductCard(Component):
    @property
    def sku(self) -> str | None:
        return self._root.get_attribute("data-product-sku")

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

    @property
    def variations_button(self) -> Locator:
        return self._root.locator(
            f"[data-test-id='variations-{self.sku}-button']"
        ).first

    def find_variation_item(self, sku: str) -> LineItem:
        return LineItem(root=self._root.locator(f"[data-item-sku='{sku}']"))
