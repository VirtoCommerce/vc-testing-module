from playwright.sync_api import Locator


class OrderSummaryComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def cart_subtotal_label(self) -> Locator:
        return self.element.locator("[data-test-id='cart-subtotal-label']")

    @property
    def cart_discount_total_label(self) -> Locator:
        return self.element.locator("[data-test-id='cart-discount-total-label']")

    @property
    def cart_tax_total_label(self) -> Locator:
        return self.element.locator("[data-test-id='cart-tax-total-label']")

    @property
    def cart_shipping_total_label(self) -> Locator:
        return self.element.locator("[data-test-id='cart-shipping-total-label']")

    @property
    def cart_total_label(self) -> Locator:
        return self.element.locator("[data-test-id='cart-total-label']")
