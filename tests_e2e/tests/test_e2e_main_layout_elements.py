import allure, os, pytest
from fixtures.anonymous_catalog_requests_fixture import AnonymousCatalogRequests
from playwright.sync_api import Page, expect
from tests_e2e.pages.home_page import HomePage
from tests_e2e.pages.sign_in_page import SignInPage



@pytest.mark.e2e
@allure.title("Main layout top header anonymous user elements presence (E2E)")
def test_e2e_main_layout_top_header_anonymous_user_elements_presence(config, page: Page, anonymous_catalog_requests: AnonymousCatalogRequests):
    print(f"{os.linesep}Running E2E test to check main layout top header anonymous user elements presence...", end=" ")

    anonymous_catalog_requests.toggle(True)

    home_page = HomePage(page, config)
    home_page.navigate()

    expect(home_page.top_header_component.language_selector_component.element).to_be_visible(), "Language selector is not visible"
    expect(home_page.top_header_component.currency_selector_component.element).to_be_visible(), "Currency selector is not visible"
    expect(home_page.top_header_component.contacts_link).to_be_visible(), "Contacts link is not visible"
    expect(home_page.top_header_component.sign_in_link).to_be_visible(), "Sign in link is not visible"
    expect(home_page.top_header_component.sign_up_link).to_be_visible(), "Sign up link is not visible"


@pytest.mark.e2e
@allure.title("Main layout top header registered user elements presence (E2E)")
def test_e2e_main_layout_top_header_registered_user_elements_presence(config, page: Page, anonymous_catalog_requests: AnonymousCatalogRequests):
    print(f"{os.linesep}Running E2E test to check main layout top header registered user elements presence...", end=" ")

    anonymous_catalog_requests.toggle(True)

    home_page = HomePage(page, config)

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(config["username"], config["password"])

    expect(page).to_have_url(home_page.url), "User is not redirected to home page after sign in"
    expect(home_page.top_header_component.language_selector_component.element).to_be_visible(), "Language selector is not visible"
    expect(home_page.top_header_component.currency_selector_component.element).to_be_visible(), "Currency selector is not visible"
    expect(home_page.top_header_component.contacts_link).to_be_visible(), "Contacts link is not visible"
    expect(home_page.top_header_component.sign_in_link).not_to_be_visible(), "Sign in link is visible"
    expect(home_page.top_header_component.sign_up_link).not_to_be_visible(), "Sign up link is visible"
