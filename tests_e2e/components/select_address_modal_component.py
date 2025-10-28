from playwright.sync_api import Locator


class SelectAddressModalComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def items(self) -> list[Locator]:
        return self.element.locator("[data-test-id^='customer-address-']").all()

    @property
    def confirm_button(self) -> Locator:
        return self.element.locator("[data-test-id='confirm-button']")

    @property
    def close_button(self) -> Locator:
        return self.element.locator("[data-test-id='close-button']")
