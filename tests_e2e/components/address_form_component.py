from playwright.sync_api import Locator


class AddressFormComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def description_input(self) -> Locator:
        return self.element.locator("[data-test-id='description']")

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

    def fill_address(self, address: dict[str, str]) -> None:
        """Fill address form. Handles both personal and company address forms."""
        # Company address forms have description field
        if "description" in address and self.description_input.count() > 0:
            self.description_input.fill(address["description"])
        
        # Personal address forms have these fields (company forms don't)
        if "first_name" in address and self.first_name_input.count() > 0:
            self.first_name_input.fill(address["first_name"])
        if "last_name" in address and self.last_name_input.count() > 0:
            self.last_name_input.fill(address["last_name"])
        if "email" in address and self.email_input.count() > 0:
            self.email_input.fill(address["email"])
        if "phone" in address and self.phone_input.count() > 0:
            self.phone_input.fill(address["phone"])
        
        # Required fields for all address forms
        self.select_country(address["country"])
        self.postal_code_input.fill(address["postal_code"])
        self.city_input.fill(address["city"])
        self.address_line_1_input.fill(address["address_line_1"])
        
        # Optional fields
        if address.get("address_line_2") and self.address_line_2_input.count() > 0:
            self.address_line_2_input.fill(address["address_line_2"])
        if "region" in address and self.region_select.count() > 0 and self.region_select.is_enabled():
            self.select_region(address["region"])

    def select_country(self, country: str) -> None:
        self.country_select.click()
        self.element.locator(f"button:has-text('{country}')").click()

    def select_region(self, region: str) -> None:
        self.region_select.click()
        self.element.locator(f"button:has-text('{region}')").click()
