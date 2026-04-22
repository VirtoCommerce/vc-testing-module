from playwright.sync_api import Locator


class AddressSelectorComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def select_address_button(self) -> Locator:
        return self.element.locator("[data-test-id='select-address-button']")

    @property
    def selected_address_label(self) -> Locator:
        return self.element.locator("[data-test-id='selected-address-label']")
