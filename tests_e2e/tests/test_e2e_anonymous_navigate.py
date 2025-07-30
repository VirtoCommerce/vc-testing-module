import allure, os, pytest, re
from playwright.sync_api import Page, expect
from fixtures.anonymous_catalog_requests_fixture import AnonymousCatalogRequests
from tests_e2e.pages.home_page import HomePage


@pytest.mark.e2e
@allure.title("Navigate application as anonymous user (E2E)")
def test_e2e_navigate_application_as_anonymous_user(config, page: Page, anonymous_catalog_requests: AnonymousCatalogRequests):
    print(f"{os.linesep}Running E2E test to navigate application as anonymous user...", end=" ")

    anonymous_catalog_requests.toggle(True)

    home_page = HomePage(page, config)
    home_page.navigate()

    expect(page).to_have_url(home_page.url)


@pytest.mark.e2e
@allure.title("Navigate application as registered user (E2E)")
def test_e2e_navigate_application_as_registered_user(config, page: Page, anonymous_catalog_requests: AnonymousCatalogRequests):
    print(f"{os.linesep}Running E2E test to navigate application as registered user...", end=" ")

    anonymous_catalog_requests.toggle(False)

    home_page = HomePage(page, config)
    home_page.navigate()

    expect(page).to_have_url(re.compile(r".*/sign-in(?:\?.*)?$"))
