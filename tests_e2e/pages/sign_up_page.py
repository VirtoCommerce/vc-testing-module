from typing import Optional
from playwright.sync_api import Locator, Page
from tests_e2e.pages.main_layout_page import MainLayoutPage


class SignUpPage(MainLayoutPage):
    def __init__(self, config: dict, page: Page):
        self.page = page
        self.config = config

    @property
    def url(self) -> str:
        return f"{self.config['frontend_base_url']}/sign-up"

    @property
    def personal_registration_radio_button(self) -> Locator:
        return self.page.locator("[data-test-id='sign-up-personal-registration-radio-button']")

    @property
    def organization_registration_radio_button(self) -> Locator:
        return self.page.locator("[data-test-id='sign-up-organization-registration-radio-button']")

    @property
    def first_name_input(self) -> Locator:
        return self.page.locator("[data-test-id='sign-up-first-name-input']")

    @property
    def last_name_input(self) -> Locator:
        return self.page.locator("[data-test-id='sign-up-last-name-input']")

    @property
    def email_input(self) -> Locator:
        return self.page.locator("[data-test-id='sign-up-email-input']")

    @property
    def organization_name_input(self) -> Locator:
        return self.page.locator("[data-test-id='sign-up-organization-name-input']")

    @property
    def password_input(self) -> Locator:
        return self.page.locator("[data-test-id='sign-up-password-input']")

    @property
    def confirm_password_input(self) -> Locator:
        return self.page.locator("[data-test-id='sign-up-confirm-password-input']")

    @property
    def submit_button(self) -> Locator:
        return self.page.locator("[data-test-id='sign-up-submit-button']")

    def navigate(self) -> None:
        self.page.goto(f"{self.config['frontend_base_url']}/sign-up")
        self.page.wait_for_load_state("networkidle")

    def select_personal_registration(self) -> None:
        self.personal_registration_radio_button.click()

    def select_organization_registration(self) -> None:
        self.organization_registration_radio_button.click()

    def sign_up(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        organization_name: Optional[str] = None,
    ) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.confirm_password_input.fill(password)

        if organization_name:
            self.organization_name_input.fill(organization_name)

        self.submit_button.click()

        self.page.wait_for_load_state("networkidle")
