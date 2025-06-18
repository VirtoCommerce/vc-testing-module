import allure, os, pytest
from playwright.sync_api import expect
from tests_e2e.pages.home_page import HomePage
from tests_e2e.pages.sign_in_page import SignInPage


@pytest.mark.e2e
@allure.feature("Sign in with valid credentials (E2E)")
def test_e2e_successful_sign_in(config, page):
    print(f"{os.linesep}Running E2E test to sign in with valid credentials...", end=" ")

    home_page = HomePage(config, page)
    sign_in_page = SignInPage(config, page)

    sign_in_page.navigate()

    sign_in_page.sign_in(config["username"], config["password"])

    expect(page).to_have_url(home_page.url)
    expect(home_page.header_component.sign_in_link).not_to_be_visible()
    expect(home_page.header_component.sign_up_link).not_to_be_visible()
    expect(home_page.header_component.dashboard_link).to_be_visible()
