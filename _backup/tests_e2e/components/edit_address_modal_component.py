from playwright.sync_api import Locator

from tests_e2e.components.address_form_component import AddressFormComponent


class EditAddressModalComponent:

    def __init__(self, element: Locator):
        self.element = element

    @property
    def address_form_component(self) -> AddressFormComponent:
        address_form = self.element.locator("[data-test-id='address-form']")
        if address_form.count() > 0:
            return AddressFormComponent(address_form)
        return AddressFormComponent(self.element)

    @property
    def submit_button(self) -> Locator:
        submit_btn = self.element.locator("[data-test-id='submit-button']")
        if submit_btn.count() > 0:
            return submit_btn
        return self.element.locator("button:has-text('Save'), button:has-text('Create')").first

    @property
    def cancel_button(self) -> Locator:
        cancel_btn = self.element.locator("[data-test-id='cancel-button']")
        if cancel_btn.count() > 0:
            return cancel_btn
        return self.element.locator("button:has-text('Cancel')")
