from playwright.sync_api import Locator, Page
from tests_e2e.components.header_component import HeaderComponent


class SignInPage:
    def __init__(self, config: dict, page: Page):
        self.page = page
        self.config = config
        self.header_component = HeaderComponent(page, config)

    @property
    def url(self) -> str:
        return f"{self.config['frontend_base_url']}/sign-in"

    @property
    def email_input(self) -> Locator:
        """Sign in page email input locator"""
        return self.page.locator("[data-test-id='sign-in-email-input']")

    @property
    def password_input(self) -> Locator:
        """Sign in page password input locator"""
        return self.page.locator("[data-test-id='sign-in-password-input']")

    @property
    def forgot_password_link(self) -> Locator:
        """Sign in page forgot password link locator"""
        return self.page.locator("[data-test-id='sign-in-forgot-password-link']")

    @property
    def login_button(self) -> Locator:
        """Sign in page login button locator"""
        return self.page.locator("[data-test-id='sign-in-login-button']")

    @property
    def sign_up_button(self) -> Locator:
        """Sign in page sign up button locator"""
        return self.page.locator("[data-test-id='sign-in-registration-button']")

    @property
    def sign_in_error_alert(self) -> Locator:
        """Sign in page error alert locator"""
        return self.page.locator("[data-test-id^='sign-in-error-'][data-test-id$='-alert']")

    def navigate(self) -> None:
        self.page.goto(f"{self.config['frontend_base_url']}/sign-in")
        self.page.wait_for_load_state("networkidle")

    def sign_in(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_load_state("networkidle")
