from playwright.sync_api import Locator

from gql.types import CartAddress

from .component import Component


class AddressForm(Component):
    @property
    def first_name_input(self) -> Locator:
        return self._root.locator("[data-test-id='first-name-input']")

    @property
    def last_name_input(self) -> Locator:
        return self._root.locator("[data-test-id='last-name-input']")

    @property
    def email_input(self) -> Locator:
        return self._root.locator("[data-test-id='email-input']")

    @property
    def phone_input(self) -> Locator:
        return self._root.locator("[data-test-id='phone-input']")

    @property
    def description_input(self) -> Locator:
        return self._root.locator("[data-test-id='description-input']")

    @property
    def country_select(self) -> Locator:
        return self._root.locator("[data-test-id='country-select']")

    @property
    def postal_code_input(self) -> Locator:
        return self._root.locator("[data-test-id='postal-code-input']")

    @property
    def region_select(self) -> Locator:
        return self._root.locator("[data-test-id='region-select']")

    @property
    def city_input(self) -> Locator:
        return self._root.locator("[data-test-id='city-input']")

    @property
    def line_1_input(self) -> Locator:
        return self._root.locator("[data-test-id='line-1-input']")

    @property
    def line_2_input(self) -> Locator:
        return self._root.locator("[data-test-id='line-2-input']")

    def select_country(self, country: str) -> None:
        self.country_select.click()
        self.country_select.locator("button").filter(has_text=country).click()

    def select_region(self, region: str) -> None:
        self.region_select.click()
        self.region_select.locator("button").filter(has_text=region).click()

    def fill(self, address: CartAddress) -> None:
        if address.first_name:
            self.first_name_input.fill(address.first_name)
        if address.last_name:
            self.last_name_input.fill(address.last_name)
        if address.phone:
            self.phone_input.fill(address.phone)
        if address.country_name:
            self.select_country(country=address.country_name)
        if address.postal_code:
            self.postal_code_input.fill(address.postal_code)
        if address.region_name:
            self.select_region(region=address.region_name)
        if address.city:
            self.city_input.fill(address.city)
        if address.line1:
            self.line_1_input.fill(address.line1)
        if address.line2:
            self.line_2_input.fill(address.line2)
        if address.email:
            self.email_input.fill(address.email)
