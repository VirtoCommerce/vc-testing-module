from playwright.sync_api import Locator

from .add_to_cart_component import AddToCartComponent


class VariationLineItemComponent:

    def __init__(self, element: Locator):
        self.element = element

    @property
    def add_to_cart_component(self) -> AddToCartComponent:
        return AddToCartComponent(self.element.locator("[data-test-id='add-to-cart-component']"))

    @property
    def name(self) -> str:
        text = self.element.locator(".vc-line-item__name").text_content()
        return text.strip() if text else ""

    @property
    def name_locator(self) -> Locator:
        return self.element.locator(".vc-line-item__name")

    @property
    def quantity_stepper_input(self) -> Locator:
        return self.element.locator("[data-test-id='quantity-stepper-input']")

    @property
    def quantity_stepper_decrement(self) -> Locator:
        return self.element.locator("[data-test-id='quantity-stepper-decrement']")

    @property
    def quantity_stepper_increment(self) -> Locator:
        return self.element.locator("[data-test-id='quantity-stepper-increment']")

    @property
    def quantity_input(self) -> Locator:
        return self.element.locator("[data-test-id='quantity-stepper-input'] input")

    @property
    def count_in_cart_label(self) -> Locator:
        return self.element.locator("[data-test-id='count-in-cart-label']")
