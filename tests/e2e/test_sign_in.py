import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import HomePage, SignInPage
from playwright.sync_api import Page, expect
from tests.context import Context

_USERNAME = "acme_store_employee_1@acme.com"


@pytest.mark.e2e
@pytest.mark.with_page_context(_USERNAME)
def test_sign_in_success(
    global_settings: GlobalSettings, page: Page, ctx: Context
) -> None:
    sign_in_page = SignInPage(global_settings=global_settings, page=page)
    sign_in_page.navigate()

    expect(sign_in_page.email_input).to_be_visible()
    expect(sign_in_page.password_input).to_be_visible()
    expect(sign_in_page.forgot_password_link).to_be_visible()
    expect(sign_in_page.sign_in_button).to_be_visible()

    sign_in_page.email_input.fill(_USERNAME)
    sign_in_page.password_input.fill(global_settings.users_password.get_secret_value())
    sign_in_page.sign_in_button.click()

    home_page = HomePage(global_settings=global_settings, page=page)
    expect(page).to_have_url(home_page.url)
    expect(home_page.top_header.account_button.root).to_be_visible()


@pytest.mark.e2e
def test_sign_in_failed(
    global_settings: GlobalSettings, page: Page, ctx: Context
) -> None:
    sign_in_page = SignInPage(global_settings=global_settings, page=page)
    sign_in_page.navigate()

    expect(sign_in_page.email_input).to_be_visible()
    expect(sign_in_page.password_input).to_be_visible()
    expect(sign_in_page.forgot_password_link).to_be_visible()
    expect(sign_in_page.sign_in_button).to_be_visible()

    sign_in_page.email_input.fill("fake-username@test.com")
    sign_in_page.password_input.fill(global_settings.users_password.get_secret_value())
    sign_in_page.sign_in_button.click()

    expect(sign_in_page.sign_in_error_alert).to_be_visible()
