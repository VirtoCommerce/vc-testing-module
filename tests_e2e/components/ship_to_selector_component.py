from playwright.sync_api import Locator


class ShipToSelectorComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def select_address_label(self) -> Locator:
        return self.element.locator("[data-test-id='select-address-label']")

    @property
    def selected_address_label(self) -> Locator:
        return self.element.locator("[data-test-id='selected-address-label']")

    @property
    def shipping_addresses_dropdown(self) -> Locator:
        return self.element.locator("[data-test-id='shipping-addresses-list']")

    @property
    def shipping_addresses(self) -> list[Locator]:
        return self.element.locator(".ship-to-selector__item").all()
