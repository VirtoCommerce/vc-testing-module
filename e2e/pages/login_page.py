from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page, config: dict):
        self.page = page
        self.config = config
        
        # Locators
        self.email_input = page.get_by_placeholder("Enter your email address")
        self.password_input = page.get_by_placeholder("Enter your password")
        self.login_button = page.get_by_role("button", name="Log in")       

    def navigate(self):
        """Navigate to login page"""
        self.page.goto(f"{self.config['base_url']}/sign-in")
        self.page.wait_for_load_state("networkidle")

    def login(self, email: str, password: str, remember: bool = False):
        """Perform login with given credentials"""
        self.email_input.fill(email)
        self.password_input.fill(password)      
        self.login_button.click()
        self.page.wait_for_load_state("networkidle")
       

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