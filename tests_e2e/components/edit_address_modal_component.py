from playwright.sync_api import Locator

from tests_e2e.components.address_form_component import AddressFormComponent


class EditAddressModalComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def address_form_component(self) -> AddressFormComponent:
        return AddressFormComponent(
            self.element.locator("[data-test-id='address-form']")
        )

    @property
    def submit_button(self) -> Locator:
        return self.element.locator("[data-test-id='submit-button']")

    @property
    def cancel_button(self) -> Locator:
        return self.element.locator("[data-test-id='cancel-button']")
