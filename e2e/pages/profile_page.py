from playwright.sync_api import Page, expect
from e2e.pages.locators.profile_locators import ProfileLocators
from e2e.pages.locators.top_header_locators import TopHeaderLocators
from playwright.sync_api import BrowserContext


class ProfilePage:
    def __init__(self, page: Page, config: dict, browser_context: BrowserContext):
        self.page = page
        self.config = config
        self.browser_context = browser_context

    def navigate(self):
        """Navigate to profile page"""
        self.page.goto(f"{self.config['frontend_base_url']}/account/profile")
        self.page.wait_for_load_state("networkidle")

    def click_dashboard(self):
        """Click dashboard"""
        self.page.click(TopHeaderLocators.DASHBOARD_LINK)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_url(f"{self.config['frontend_base_url']}/account/dashboard")

    def click_profile(self):
        """Click profile"""
        self.page.click(ProfileLocators.PROFILE_LINK)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_url(f"{self.config['frontend_base_url']}/account/profile")

    def change_currency(self, currency: str):
        """Change currency"""
        self.page.click(ProfileLocators.CURRENCY_SELECTOR)
        if currency == "USD":
            self.page.click(ProfileLocators.CURRENCY_SELECTOR_OPTION_USD)
        elif currency == "EUR":
            self.page.click(ProfileLocators.CURRENCY_SELECTOR_OPTION_EUR)
        currency_input = self.page.locator(ProfileLocators.DEFAULT_CURRENCY.format(currency))
        expect(currency_input).to_have_attribute("placeholder", currency)
        self.page.wait_for_load_state("networkidle")

    def change_language(self, language: str):
        """Change language"""
        self.page.click(ProfileLocators.LANGUAGE_SELECTOR)
        self.page.click(f"text={language}")
        self.page.wait_for_load_state("networkidle")

    def update_profile(self):
        """Click update button"""
        self.page.click(ProfileLocators.UPDATE_BUTTON)
        self.page.wait_for_selector(ProfileLocators.DIALOG_MODAL)
        self.page.click(ProfileLocators.BUTTON_OK)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state("domcontentloaded")
