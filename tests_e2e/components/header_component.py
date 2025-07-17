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
    
    def language_item(self, language: str) -> Locator:
        """Top header language item selector locator"""
        return self.page.locator(f"[data-test-id='language-selector-item-{language}']")

    @property
    def current_language_label(self) -> Locator:
        """Top header current language label locator"""
        return self.page.locator("[data-test-id='current-language-label']")

    @property
    def currency_selector(self) -> Locator:
        """Top header currency selector locator"""
        return self.page.locator("[data-test-id='currency-selector-button']")
    
    def currency_item(self, currency: str) -> Locator:
        """Top header currency item selector locator"""
        return self.page.locator(f"[data-test-id='currency-selector-item-{currency}']")

    @property
    def current_currency_label(self) -> Locator:
        """Top header current currency label locator"""
        return self.page.locator("[data-test-id='current-currency-label']")

    @property
    def ship_to_selector(self) -> Locator:
        """Top header ship to selector locator"""
        return self.page.locator("[data-test-id='ship-to-selector-button']")
    
    @property
    def customer_name_label(self) -> Locator:
        """Top header customer name label locator"""
        return self.page.locator("[data-test-id='customer-name-label']")
    
    @property
    def account_menu_button(self) -> Locator:
        """Top header account menu button locator"""
        return self.page.locator("[data-test-id='account-menu-button']")
    
    @property
    def sign_out_button(self) -> Locator:
        """Top header sign out button locator"""
        return self.page.locator("[data-test-id='sign-out-button']")
    
    def sign_out(self) -> None:
        """Sign out from top header"""
        self.customer_name_label.wait_for(state="visible")
        self.account_menu_button.click()
        self.sign_out_button.wait_for(state="visible")
        self.sign_out_button.click()
        self.page.wait_for_load_state("networkidle")
    
    def select_language(self, language: str) -> None:
        """Select language in top header"""
        self.language_selector.click()
        self.language_item(language).click()
        self.current_language_label.wait_for(state="visible")
        self.page.wait_for_load_state("networkidle")
    
    def select_currency(self, currency: str) -> None:
        """Select currency in top header"""
        self.currency_selector.click()
        self.currency_item(currency).click()
        self.current_currency_label.wait_for(state="visible")
        self.page.wait_for_load_state("networkidle")
