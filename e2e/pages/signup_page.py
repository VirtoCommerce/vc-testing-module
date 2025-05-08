from playwright.sync_api import Page, BrowserContext, expect
from typing import Optional, List
from e2e.pages.locators.signup_locators import SignupLocators
from utils.commonLocators.common_components_locators import CommonComponentsLocators

class RegistrationPage:
    def __init__(self, page: Page, config: dict, browser_context: BrowserContext):
        self.page = page  
        self.config = config
        self.browser_context = browser_context
    
    def navigate(self):
        """Navigate to the signup page"""
        self.page.goto(f"{self.config['base_url']}/sign-up")
     

    def select_company_account(self):
        """Select the company account radio button"""
        self.page.click(SignupLocators.COMPANY_RADIO_BUTTON)
        expect(self.page.locator(SignupLocators.COMPANY_RADIO_BUTTON)).to_be_checked()
        expect(self.page.locator(SignupLocators.COMPANY_ACCOUNT_LABEL)).to_have_text("Company account")

    def fill_registration_form(self, first_name: str, last_name: str, email: str, 
                             organization_name: str, password: str, confirm_password: str):
        """Fill in the registration form with provided details"""
        self.page.locator(SignupLocators.FIRST_NAME_INPUT).type(first_name, delay=100)
        self.page.locator(SignupLocators.LAST_NAME_INPUT).type(last_name, delay=100)
        self.page.locator(SignupLocators.EMAIL_INPUT).type(email, delay=100)
        self.page.locator(SignupLocators.ORGANIZATION_NAME_INPUT).type(organization_name, delay=100)
        self.page.locator(SignupLocators.PASSWORD_INPUT).type(password, delay=100)
        self.page.locator(SignupLocators.CONFIRM_PASSWORD_INPUT).type(confirm_password, delay=100)

    def click_sign_up(self):
        """Click the sign up button"""
        self.page.locator(SignupLocators.SIGN_UP_BUTTON).click()
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden", timeout=10000)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_url(f'{self.config["base_url"]}/successful-registration')
    
    def click_sign_up_button(self):
        """Click the sign up button"""
        self.page.locator(SignupLocators.SIGN_UP_BUTTON).click()
        self.page.wait_for_timeout(3000)
        

    def is_success_message_visible(self) -> bool:
        """Check if registration success message is visible"""         
        expect(self.page).to_have_url(f'{self.config["base_url"]}/successful-registration')
        expect(self.page.locator(SignupLocators.REGISTRATION_COMPLETED_TITLE)).to_contain_text('Registration completed')
        return self.page.locator(SignupLocators.REGISTRATION_COMPLETED_TITLE).is_visible()
       

    def click_home_page(self):
        """Click the home page button"""
        self.page.locator(SignupLocators.HOME_PAGE_BUTTON).click() 

    def is_password_error_visible(self) -> bool:
        """Check if password error message is visible"""
        error_elements = self.page.locator(SignupLocators.PASSWORD_ERROR_MESSAGE).all()
        if not error_elements:
            return False
        return any(element.is_visible() for element in error_elements)

    def get_password_error_text(self) -> str:
        """Get the password error message text"""
        error_element = self.page.locator(SignupLocators.PASSWORD_ERROR_MESSAGE)
        expect(error_element).to_be_visible()
        return error_element.text_content()

    def get_all_password_error_texts(self) -> List[str]:
        """Get all password error message texts"""
        error_elements = self.page.locator(SignupLocators.PASSWORD_ERROR_MESSAGE).all()
        return [element.text_content() for element in error_elements]

    def clear_registration_form(self):
        """Clear all fields in the registration form"""
        # Clear text inputs
        self.page.locator(SignupLocators.FIRST_NAME_INPUT).clear()
        self.page.locator(SignupLocators.LAST_NAME_INPUT).clear()
        self.page.locator(SignupLocators.EMAIL_INPUT).clear()
        self.page.locator(SignupLocators.ORGANIZATION_NAME_INPUT).clear()
        self.page.locator(SignupLocators.PASSWORD_INPUT).clear()
        self.page.locator(SignupLocators.CONFIRM_PASSWORD_INPUT).clear()       
    
    