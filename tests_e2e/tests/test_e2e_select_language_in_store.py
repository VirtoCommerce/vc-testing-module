import allure, os, pytest,re
from playwright.sync_api import expect
from tests_e2e.pages.sign_in_page import SignInPage
from tests_e2e.components.header_component import HeaderComponent
from tests_e2e.pages.home_page import HomePage


@pytest.mark.e2e
@allure.feature("Select language in store (E2E)")
def test_e2e_select_language_in_store(config, page):
    print(f"{os.linesep}Running E2E test to select language in store...", end=" ")

    sign_in_page = SignInPage(page, config)
    header_component = HeaderComponent(page, config)
    home_page = HomePage(page, config)

    sign_in_page.navigate()

    sign_in_page.sign_in(config["front_admin"], config["password"])

    expect(page).to_have_url(home_page.url)
    expect(header_component.sign_in_link).not_to_be_visible()
    expect(header_component.sign_up_link).not_to_be_visible()
    expect(header_component.dashboard_link).to_be_visible()

    expect(header_component.language_selector).to_be_visible()
    expect(header_component.current_language_label).to_have_text("en")

    header_component.select_language("de")

    expect(header_component.current_language_label).to_have_text("de")

    header_component.sign_out()

    expect(header_component.sign_in_link).to_be_visible()
    expect(header_component.sign_up_link).to_be_visible()

    expect(header_component.language_selector).to_be_visible()
    expect(header_component.current_language_label).to_have_text("en")
    




    

 
