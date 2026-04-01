from playwright.sync_api import Locator

from .component import Component


class ShippingAddressSection(Component):
    @property
    def select_address_button(self) -> Locator:
        return self._root.locator("[data-test-id='select-address-button']")

    @property
    def current_address_label(self) -> Locator:
        return self._root.locator("[data-test-id='selected-address-label']")
