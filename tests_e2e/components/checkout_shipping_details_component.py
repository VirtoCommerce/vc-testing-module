from typing import Literal
from playwright.sync_api import Locator
from tests_e2e.components.address_selector_component import AddressSelectorComponent


class CheckoutShippingDetailsComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def pickup_delivery_option_switcher(self) -> Locator:
        return self.element.locator("[data-test-id='checkout.shipping-details-section.pickup-switcher']")

    @property
    def shipping_delivery_option_switcher(self) -> Locator:
        return self.element.locator("[data-test-id='checkout.shipping-details-section.shipping-switcher']")

    @property
    def pickup_point_section(self) -> Locator:
        return self.element.locator("[data-test-id='checkout.shipping-details-section.pickup-point-section']")

    @property
    def address_selector_component(self) -> AddressSelectorComponent:
        return AddressSelectorComponent(self.element.locator("[data-test-id='checkout.shipping-details-section.shipping-address-section']"))

    @property
    def shipping_method_selector(self) -> Locator:
        return self.element.locator("[data-test-id='checkout.shipping-details-section.shipping-method-selector']")

    def switch_delivery_option(self, option: Literal["pickup", "shipping"]) -> None:
        if option == "pickup":
            self.pickup_delivery_option_switcher.click()
        elif option == "shipping":
            self.shipping_delivery_option_switcher.click()

    def select_shipping_method(self, shipping_method: str) -> None:
        self.shipping_method_selector.click()
        self.element.locator(f"[data-shipping-method-id='{shipping_method}']").click()
