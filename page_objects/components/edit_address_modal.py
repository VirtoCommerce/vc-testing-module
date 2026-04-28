from playwright.sync_api import Locator

from .address_form import AddressForm
from .component import Component


class EditAddressModal(Component):
    @property
    def address_form(self) -> AddressForm:
        return AddressForm(root=self._root.locator("[data-test-id='address-form']"))

    @property
    def submit_button(self) -> Locator:
        return self._root.locator("[data-test-id='submit-button']")

    @property
    def cancel_button(self) -> Locator:
        return self._root.locator("[data-test-id='cancel-button']")
