from playwright.sync_api import Locator

from page_objects.layouts.main import MainLayout


class SignInPage(MainLayout):
    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/sign-in"

    @property
    def email_input(self) -> Locator:
        return self._page.locator("[data-test-id='email-input']")

    @property
    def password_input(self) -> Locator:
        return self._page.locator("[data-test-id='password-input']")

    @property
    def forgot_password_link(self) -> Locator:
        return self._page.locator("[data-test-id='forgot-password-link']")

    @property
    def sign_in_button(self) -> Locator:
        return self._page.locator("[data-test-id='login-button']")

    @property
    def sign_in_error_alert(self) -> Locator:
        return self._page.locator("[data-test-id='sign-in-error-alert']")

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")
