import allure, os, pytest
from playwright.sync_api import expect
from tests_e2e.pages.sign_in_page import SignInPage
from tests_e2e.components.header_component import HeaderComponent
from tests_e2e.pages.home_page import HomePage
from graphql_operations.store.store_operations import StoreOperations


@pytest.mark.e2e
@allure.feature("Select language in store (E2E)")
def test_e2e_select_language_in_store(config, page, graphql_client):
    print(f"{os.linesep}Running E2E test to select language in store...", end=" ")

    sign_in_page = SignInPage(page, config)
    header_component = HeaderComponent(page, config)
    home_page = HomePage(page, config)
    store_operations = StoreOperations(graphql_client)

    sign_in_page.navigate()

    sign_in_page.sign_in(config["front_admin"], config["password"])

    expect(page).to_have_url(home_page.url)
    expect(header_component.sign_in_link).not_to_be_visible()
    expect(header_component.sign_up_link).not_to_be_visible()
    expect(header_component.dashboard_link).to_be_visible()

    frontend_domain = config["frontend_base_url"].split("//")[1]
    store = store_operations.get_store(domain=frontend_domain)

    if store["defaultLanguage"]["cultureName"] == "en-US":
        expect(header_component.language_selector).to_be_visible()
        expect(header_component.current_language_label).to_have_text(store["defaultLanguage"]["twoLetterLanguageName"])

    german_language = next((lang for lang in store["availableLanguages"] if lang["cultureName"] == "de-DE"), None)
    if german_language:
       header_component.select_language(german_language["twoLetterLanguageName"])
       expect(header_component.current_language_label).to_have_text(german_language["twoLetterLanguageName"])
    else:
        print(f"{os.linesep}German language not found in store available languages")    

    header_component.sign_out()
    expect(header_component.sign_in_link).to_be_visible()
    expect(header_component.sign_up_link).to_be_visible()

    expect(header_component.language_selector).to_be_visible()
    expect(header_component.current_language_label).to_have_text(store["defaultLanguage"]["twoLetterLanguageName"])



    

 
