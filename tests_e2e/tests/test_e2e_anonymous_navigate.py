import allure, os, pytest, re
from gql import Client
from playwright.sync_api import Page, expect
from graphql_operations.store.store_operations import StoreOperations
from tests_e2e.pages.home_page import HomePage


@pytest.mark.e2e
@allure.feature("Navigate application as anonymous user (E2E)")
def test_e2e_navigate_application_as_anonymous_user(config, page: Page, graphql_client: Client):
    print(f"{os.linesep}Running E2E test to navigate application as anonymous user...", end=" ")

    home_page = HomePage(config, page)
    store_operations = StoreOperations(graphql_client)

    frontend_domain = config["frontend_base_url"].split("//")[1]
    store = store_operations.get_store(domain=frontend_domain)

    home_page.navigate()

    if store["settings"]["anonymousUsersAllowed"]:
        expect(page).to_have_url(home_page.url)
    else:
        expect(page).to_have_url(re.compile(r".*/sign-in(?:\?.*)?$"))
