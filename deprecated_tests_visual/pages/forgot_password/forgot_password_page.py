from .forgot_password_locators import ForgotPasswordLocators


class ForgotPasswordPage:
    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.locators = ForgotPasswordLocators()

    def navigate(self):
        """Navigate to forgot password page"""
        self.page.goto(f"{self.config['base_url']}/forgot-password")
        self.page.wait_for_selector(self.locators.EMAIL_INPUT, state="visible", timeout=10000)
