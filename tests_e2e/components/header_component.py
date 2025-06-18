from playwright.sync_api import Locator, Page


class HeaderComponent:
    def __init__(self, page: Page, config: dict):
        self.page = page
        self.config = config

    @property
    def sign_in_link(self) -> Locator:
        """Top header sign in link locator"""
        return self.page.locator("[data-test-id='sign-in-link']")

    @property
    def sign_up_link(self) -> Locator:
        """Top header sign up link locator"""
        return self.page.locator("[data-test-id='sign-up-link']")

    @property
    def dashboard_link(self) -> Locator:
        """Top header dashboard link locator"""
        return self.page.locator("[data-test-id='dashboard-link']")

    @property
    def contacts_link(self) -> Locator:
        """Top header contacts link locator"""
        return self.page.locator("[data-test-id='contacts-link']")

    @property
    def support_phone_number_link(self) -> Locator:
        """Top header support phone number link locator"""
        return self.page.locator("[data-test-id='support-phone-number-link']")

    @property
    def language_selector(self) -> Locator:
        """Top header language selector locator"""
        return self.page.locator("[data-test-id='language-selector-button']")

    @property
    def currency_selector(self) -> Locator:
        """Top header currency selector locator"""
        return self.page.locator("[data-test-id='currency-selector-button']")

    @property
    def ship_to_selector(self) -> Locator:
        """Top header ship to selector locator"""
        return self.page.locator("[data-test-id='ship-to-selector-button']")
