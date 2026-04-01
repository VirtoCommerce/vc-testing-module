from playwright.sync_api import Locator

from .component import Component


class SelectAddressModal(Component):
    @property
    def ok_button(self) -> Locator:
        return self._root.locator("[data-test-id='confirm-button']")

    @property
    def cancel_button(self) -> Locator:
        return self._root.locator("[data-test-id='close-button']")

    @property
    def addresses(self) -> Locator:
        return self._root.locator("[data-test-id^='customer-address-']")

    def find_address(self, text: str) -> Locator:
        return self.addresses.filter(has_text=text)
