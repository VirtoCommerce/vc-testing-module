import os

import allure
import pytest
from playwright.sync_api import Page, expect

from graphql_operations.store.store_operations import StoreOperations
from tests_e2e.pages.home_page import HomePage
from tests_e2e.pages.sign_in_page import SignInPage


@pytest.mark.e2e
@pytest.mark.parametrize("language", ["de-DE", "fr-FR", "it-IT"])
@allure.feature("Select language in store (E2E)")
def test_e2e_select_language_in_store(config, page: Page, graphql_client, language):
    print(f"{os.linesep}Running E2E test to select language in store...", end=" ")

    sign_in_page = SignInPage(page, config)
    home_page = HomePage(page, config)
    store_operations = StoreOperations(graphql_client)

    sign_in_page.navigate()

    sign_in_page.sign_in(config["username"], config["password"])

    expect(page).to_have_url(home_page.url)
    expect(home_page.top_header_component.sign_in_link).not_to_be_visible()
    expect(home_page.top_header_component.sign_up_link).not_to_be_visible()
    expect(home_page.top_header_component.dashboard_link).to_be_visible()

    frontend_domain = config["frontend_base_url"].split("//")[1]
    store = store_operations.get_store(domain=frontend_domain)

    if store["defaultLanguage"]["cultureName"] == "en-US":
        expect(
            home_page.top_header_component.language_selector_component.element
        ).to_be_visible()
        expect(
            home_page.top_header_component.language_selector_component.current_language_label
        ).to_have_text(store["defaultLanguage"]["twoLetterLanguageName"])

    language = next(
        (
            lang
            for lang in store["availableLanguages"]
            if lang["cultureName"] == language
        ),
        None,
    )
    if language:
        home_page.change_language(language["twoLetterLanguageName"])
        expect(
            home_page.top_header_component.language_selector_component.current_language_label
        ).to_have_text(language["twoLetterLanguageName"])
    else:
        print(f"{os.linesep}Language {language} not found in store available languages")

    home_page.sign_out()
    expect(home_page.top_header_component.sign_in_link).to_be_visible()
    expect(home_page.top_header_component.sign_up_link).to_be_visible()

    expect(
        home_page.top_header_component.language_selector_component.element
    ).to_be_visible()
    expect(
        home_page.top_header_component.language_selector_component.current_language_label
    ).to_have_text(store["defaultLanguage"]["twoLetterLanguageName"])
