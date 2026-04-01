from playwright.sync_api import Locator

from .component import Component
from .pickup_location_section import PickupLocationSection
from .shipping_address_section import ShippingAddressSection


class ShippingDetailsSection(Component):
    @property
    def pickup_switcher(self) -> Locator:
        return self._root.locator("[data-test-id='pickup-switcher']")

    @property
    def shipping_switcher(self) -> Locator:
        return self._root.locator("[data-test-id='shipping-switcher']")

    @property
    def shipping_address_section(self) -> ShippingAddressSection:
        return ShippingAddressSection(
            root=self._root.locator("[data-test-id='shipping-address-section']")
        )

    @property
    def pickup_location_section(self) -> PickupLocationSection:
        return PickupLocationSection(
            root=self._root.locator("[data-test-id='pickup-location-section']")
        )

    @property
    def shipping_method_selector(self) -> Locator:
        return self._root.locator("[data-test-id='shipping-method-selector']")

    def find_selected_shipping_method(self, code: str) -> Locator:
        return self._root.locator(f"[data-selected-shipping-method-id='{code}']")

    def select_shipping_method(self, code: str) -> None:
        self.shipping_method_selector.click()
        self._root.locator(f'[data-shipping-method-id="{code}"]').click()
