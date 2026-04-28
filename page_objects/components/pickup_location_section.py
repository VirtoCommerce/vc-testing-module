from .component import Component


class PickupLocationSection(Component):
    @property
    def select_address_button(self):
        return self._root.locator("[data-test-id='select-address-button']")
