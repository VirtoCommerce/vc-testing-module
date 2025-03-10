from .registration_locators import RegistrationLocators


class RegistrationPage:
    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.locators = RegistrationLocators()

    def navigate_to_registration_public(self):
        """Navigate to public sector registration page"""
        self.page.goto(f"{self.config['base_url']}/sign-up")        


    def click_personal_account_button(self):
        """Click on the personal account button"""
        self.page.locator(self.locators.PERSONAL_ACCOUNT_BUTTON).click()

    def click_company_account_button(self):
        """Click on the company account button"""
        self.page.locator(self.locators.COMPANY_ACCOUNT_BUTTON).click()
