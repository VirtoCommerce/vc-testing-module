from playwright.sync_api import Locator

from .address import Address
from .component import Component


class ShipToSelector(Component):
    @property
    def selected_address_label(self) -> Locator:
        return self._root.locator("[data-test-id='selected-address-label']")

    @property
    def addresses_list(self) -> Locator:
        return self._root.locator("[data-test-id='shipping-addresses-list']")

    @property
    def addresses(self) -> Locator:
        return self.addresses_list.locator("button")

    def find_address(
        self,
        postal_code: str | None = None,
        country_name: str | None = None,
        region_name: str | None = None,
        city: str | None = None,
        line_1: str | None = None,
    ) -> Address | None:
        buttons = self.addresses
        for i in range(buttons.count()):
            address = Address(root=buttons.nth(i))
            if postal_code is not None and address.postal_code != postal_code:
                continue
            if country_name is not None and address.country_name != country_name:
                continue
            if region_name is not None and address.region_name != region_name:
                continue
            if city is not None and address.city != city:
                continue
            if line_1 is not None and address.address_line_1 != line_1:
                continue
            return address
        return None