from playwright.sync_api import Locator


class LineItemComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def sku(self) -> str:
        return self.element.get_attribute("data-product-sku")

    @property
    def quantity_input(self) -> Locator:
        return self.element.locator("[data-test-id='quantity-input']")

    @property
    def remove_button(self) -> Locator:
        return self.element.locator("[data-test-id='remove-item-button']")
