import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from tests_e2e.pages.home_page import HomePage
from tests_e2e.pages.main_layout_page import MainLayoutPage
from tests_e2e.pages.sign_in_page import SignInPage


@pytest.mark.e2e
@allure.title("Switch between organizations (E2E)")
def test_e2e_switch_between_organizations(config: dict[str, Any], dataset: dict[str, Any], page: Page):
    print(f"{os.linesep}Running E2E test to switch between organizations...", end=" ")

    sign_in_page = SignInPage(page, config) 
    home_page = HomePage(page, config)   
    
    dataset_user = dataset["users"][0] 
    organization_name = dataset["organizations"][0]["name"]
    organization_name2 = dataset["organizations"][1]["name"]
       
    sign_in_page.navigate()

    sign_in_page.sign_in(dataset_user["userName"], config["users_password"])
    organization_selector = home_page.top_header_component.account_menu_component   

    home_page.top_header_component.account_menu_button.click()    
    expect(home_page.top_header_component.account_menu).to_be_visible(), "Account menu is not visible" 

    number_of_organizations = len(organization_selector.organization_selector_items)
    assert number_of_organizations == 3, f"Number of organizations is not 3, but {number_of_organizations}"


    current_organization = home_page.top_header_component.organization_name_label.text_content()
    print(f"Current organization is {current_organization}")

    if current_organization != organization_name:
        organization_selector.get_radio_button_of_organization(organization_name).click()
        page.wait_for_load_state("networkidle")
        expect(home_page.top_header_component.organization_name_label).to_have_text(organization_name), f"Current organization is not '{organization_name}'"
        home_page.top_header_component.account_menu_button.click()
        expect(organization_selector.get_radio_button_of_organization(organization_name)).to_have_attribute("aria-checked", "true"), f"Organization '{organization_name}' is not selected"
    elif current_organization != organization_name2:
        organization_selector.get_radio_button_of_organization(organization_name2).click()
        page.wait_for_load_state("networkidle")
        expect(home_page.top_header_component.organization_name_label).to_have_text(organization_name2), f"Current organization is not '{organization_name2}'"
        home_page.top_header_component.account_menu_button.click()
        expect(organization_selector.get_radio_button_of_organization(organization_name2)).to_have_attribute("aria-checked", "true"), f"Organization '{organization_name2}' is not selected"


  
