from playwright.sync_api import Page, expect, BrowserContext
from e2e.pages.locators.login_locators import LoginLocators


class LoginPage:
    def __init__(self, page: Page, config: dict = None, browser_context: BrowserContext = None):
        self.page = page
        self.config = config
        self.browser_context = browser_context
        
        # Locators
        self.email_input = page.locator(LoginLocators.EMAIL_INPUT)
        self.password_input = page.locator(LoginLocators.PASSWORD_INPUT)
        self.login_button = page.locator(LoginLocators.LOGIN_BUTTON)

    def navigate(self):
        """Navigate to the login page"""
        if self.config:
            self.page.goto(self.config["base_url"] + "/sign-in")
        else:
            self.page.goto("/sign-in")
        self.page.wait_for_load_state("networkidle")

    def login(self, email: str, password: str):
        """Login with the provided credentials"""
        
        self.page.fill(LoginLocators.EMAIL_INPUT, email)
        self.page.fill(LoginLocators.PASSWORD_INPUT, password)
        
        # Click the login button
        self.page.click(LoginLocators.LOGIN_BUTTON)
        
        # Wait for navigation to complete
        self.page.wait_for_load_state("networkidle")
        
        # Verify login was successful
        try:
            self.page.wait_for_selector(LoginLocators.ACCOUNT_ICON, state="visible", timeout=5000)
            print("Login successful")
            return True
        except:
            print("Login failed")
            return False

    def logout(self):
        """Logout from the current session"""
        try:
            # Click on the account icon
            self.page.click(LoginLocators.ACCOUNT_ICON)
            self.page.wait_for_timeout(500)
            
            # Click on the logout button
            self.page.click(LoginLocators.LOGOUT_BUTTON)
            
            # Wait for navigation to complete
            self.page.wait_for_load_state("networkidle")
            
            # Verify logout was successful
            try:
                self.page.wait_for_selector(LoginLocators.SIGN_IN_TOP, state="visible", timeout=5000)
                print("Logout successful")
                return True
            except:
                print("Logout failed")
                return False
        except Exception as e:
            print(f"Error during logout: {str(e)}")
            return False

    def expect_validation_error(self, message: str):
        """Verify validation error message"""
        error = self.page.get_by_text(message)
        expect(error).to_be_visible()
    
    def expect_validation_message(self, message: str, field: str):
        """Verify validation message for a specific field"""
        error = self.page.locator(f"div.vc-input-details__message").nth(0) if field == "email" else self.page.locator(f"div.vc-input-details__message").nth(1)
        expect(error).to_have_text(message)

    def expect_successful_login(self):
        """Verify successful login"""
        # Use regex pattern to match URL with or without trailing slash
        expect(self.page).to_have_url(f"{self.config['base_url']}/")

    def expect_form_elements_visible(self):
        """Verify all form elements are visible"""
        expect(self.email_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.login_button).to_be_visible()     