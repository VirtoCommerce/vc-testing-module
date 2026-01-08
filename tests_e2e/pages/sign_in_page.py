from playwright.sync_api import Locator, Page

from fixtures.config import Config
from tests_e2e.pages import MainLayoutPage


class SignInPage(MainLayoutPage):
    def __init__(self, page: Page, config: Config):
        self.page = page
        self.config = config

    @property
    def url(self) -> str:
        return f"{self.config['FRONTEND_BASE_URL']}/sign-in"

    @property
    def email_input(self) -> Locator:
        return self.page.locator("[data-test-id='sign-in-page.email-input']")

    @property
    def password_input(self) -> Locator:
        return self.page.locator("[data-test-id='sign-in-page.password-input']")

    @property
    def forgot_password_link(self) -> Locator:
        return self.page.locator("[data-test-id='sign-in-page.forgot-password-link']")

    @property
    def login_button(self) -> Locator:
        return self.page.locator("[data-test-id='sign-in-page.login-button']")

    @property
    def sign_up_button(self) -> Locator:
        return self.page.locator("[data-test-id='sign-in-page.sign-up-button']")

    @property
    def sign_in_error_alert(self) -> Locator:
        return self.page.locator(
            "[data-test-id^='sign-in-page.sign-in-error-'][data-test-id$='-alert']"
        )

    def navigate(self) -> None:
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    def sign_in(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_load_state("networkidle")
