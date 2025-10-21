from playwright.sync_api import Locator


class AddressFormComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def first_name_input(self) -> Locator:
        return self.element.locator("[data-test-id='first-name']")

    @property
    def last_name_input(self) -> Locator:
        return self.element.locator("[data-test-id='last-name']")

    @property
    def email_input(self) -> Locator:
        return self.element.locator("[data-test-id='email']")

    @property
    def phone_input(self) -> Locator:
        return self.element.locator("[data-test-id='phone']")

    @property
    def country_select(self) -> Locator:
        return self.element.locator("[data-test-id='country']")

    @property
    def postal_code_input(self) -> Locator:
        return self.element.locator("[data-test-id='postal-code']")

    @property
    def region_select(self) -> Locator:
        return self.element.locator("[data-test-id='region']")

    @property
    def city_input(self) -> Locator:
        return self.element.locator("[data-test-id='city']")

    @property
    def address_line_1_input(self) -> Locator:
        return self.element.locator("[data-test-id='line-1']")

    @property
    def address_line_2_input(self) -> Locator:
        return self.element.locator("[data-test-id='line-2']")
