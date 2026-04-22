from playwright.sync_api import Locator

from .add_to_cart_component import AddToCartComponent
from .quantity_stepper_component import QuantityStepperComponent
from .variation_line_item_component import VariationLineItemComponent


class ProductCardComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def sku(self) -> str:
        return self.element.get_attribute("data-product-sku")

    @property
    def add_to_cart_component(self) -> AddToCartComponent:
        return AddToCartComponent(self.element.locator("[data-test-id='add-to-cart-component']"))

    @property
    def quantity_stepper_component(self) -> QuantityStepperComponent:
        return QuantityStepperComponent(self.element.locator(".vc-quantity-stepper__input"))

    @property
    def count_in_cart_label(self) -> Locator:
        return self.element.locator("[data-test-id='count-in-cart-label']")

    @property
    def variations_button(self) -> Locator:
        return self.element.locator("[data-test-id='product-card-variations-button']")

    @property
    def variants_wrapper(self) -> Locator:
        return self.element.locator("[data-test-id='product-card-variants-wrapper']")

    @property
    def variation_line_items(self) -> list[VariationLineItemComponent]:
        return [
            VariationLineItemComponent(item)
            for item in self.variants_wrapper.locator("[data-test-id='line-item']").all()
        ]

    def get_variation_line_item_by_name(self, name: str) -> VariationLineItemComponent | None:
        for item in self.variation_line_items:
            if item.name == name:
                return item
        return None
