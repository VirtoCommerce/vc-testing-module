import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from tests_e2e.pages.home_page import HomePage
from tests_e2e.pages.sign_in_page import SignInPage


def get_user_organization_count(dataset: dict[str, Any], user: dict[str, Any]) -> int:
    """
    Get the expected number of organizations for a user from the dataset.
    
    Args:
        dataset: The dataset containing contacts and organizations
        user: The user object from the dataset
        
    Returns:
        The number of organizations the user has access to
    """
    member_id = user.get("memberId")
    if not member_id:
        return 0
    
    contacts = dataset.get("contacts", [])
    user_contact = next(
        (contact for contact in contacts if contact.get("id") == member_id),
        None
    )
    return len(user_contact.get("organizations", [])) if user_contact else 0


@pytest.mark.e2e
@allure.title("Switch between organizations (E2E)")
def test_e2e_switch_between_organizations(config: dict[str, Any], dataset: dict[str, Any], page: Page):
    print(f"{os.linesep}Running E2E test to switch between organizations...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    sign_in_page = SignInPage(page, config) 
    home_page = HomePage(page, config)   
    
    dataset_user = dataset["users"][0] 
    expected_org_count = get_user_organization_count(dataset, dataset_user)
       
    sign_in_page.navigate()

    sign_in_page.sign_in(dataset_user["userName"], config["users_password"])

    organization_list = home_page.top_header_component.account_menu_component.organization_list  
    organization_selector = home_page.top_header_component.account_menu_component  

    home_page.top_header_component.account_menu_button.click()    

    expect(organization_list).to_be_visible(), "Organization list is not visible" 
    page.wait_for_load_state("networkidle")

    number_of_organizations = len(organization_selector.organization_selector_items)
    assert number_of_organizations == expected_org_count, f"Number of organizations is not {expected_org_count}, but {number_of_organizations}" 


    current_organization = home_page.top_header_component.organization_name_label.text_content()
    print(f"Current organization is {current_organization}")
    for organization in organization_selector.organization_selector_items:
        if organization.text_content() == current_organization:           
           expect(organization.locator("input")).to_have_attribute("aria-checked", "true"), f"Organization '{organization.text_content()}' is not selected"
    
    
    organization_items = organization_selector.organization_selector_items
    current_name = current_organization

    for organization in organization_items:
        org_name = organization.text_content().strip()

        if org_name != current_name:
            selected_organization = organization

            expect(
                selected_organization.locator("input"),
                f"Organization '{org_name}' is already selected"
            ).to_have_attribute("aria-checked", "false")

            selected_organization.locator("input").click()
            page.wait_for_load_state("networkidle")

            expect(
                home_page.top_header_component.organization_name_label,
                f"Current organization should be '{org_name}'"
            ).to_have_text(org_name)

            home_page.top_header_component.account_menu_button.click()
            page.wait_for_selector(
                "[data-test-id^='main-layout.top-header.account-menu.organization-selector-item-']",
                timeout=30000
            )

            organization_selector = home_page.top_header_component.account_menu_component
            refreshed_items = organization_selector.organization_selector_items
            target_item = next(
                (
                    item
                    for item in refreshed_items
                    if item.text_content().strip() == org_name
                ),
                None
            )
            assert target_item, f"Organization '{org_name}' item not found after switching"

            expect(
                target_item.locator("input"),
                f"Organization '{org_name}' did not become selected"
            ).to_have_attribute("aria-checked", "true")
            
            break   


@pytest.mark.e2e
@allure.title("Search the organization in the list")
def test_e2e_search_organization_in_list(config: dict[str, Any], dataset: dict[str, Any], page: Page):
    print(f"{os.linesep}Running E2E test to search the organization in the list...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    sign_in_page = SignInPage(page, config) 
    home_page = HomePage(page, config)   
    
    dataset_user = dataset["users"][9]
    organization_name = dataset["organizations"][3]["name"]
    expected_org_count = get_user_organization_count(dataset, dataset_user)
       
    sign_in_page.navigate()

    sign_in_page.sign_in(dataset_user["userName"], config["users_password"])
    organization_list = home_page.top_header_component.account_menu_component.organization_list   

    home_page.top_header_component.account_menu_button.click()
    expect(organization_list).to_be_visible(), "Organization list is not visible" 
    page.wait_for_load_state("networkidle")

    organization_selector_items = home_page.top_header_component.account_menu_component.organization_selector_items
    number_of_organizations = len(organization_selector_items)

    assert number_of_organizations == expected_org_count, f"Number of organizations is not {expected_org_count}, but {number_of_organizations}"

    search_input = home_page.top_header_component.account_menu_component.search_organization
    search_input.fill(organization_name)
    search_input.press("Enter")
    page.wait_for_timeout(3000)   

    organization_item = home_page.top_header_component.account_menu_component.organization_selector_item(organization_name)
    organization_selector_items_after_search = home_page.top_header_component.account_menu_component.organization_selector_items  

    expect(organization_list).to_be_visible()
    expect(organization_item).to_contain_text(organization_name)
    number_of_organizations_after_search = len(organization_selector_items_after_search)  

    # Note: This assertion verifies the search functionality. The expected count of 2 is based on
    # the UI's search behavior with the specific search term and user's organization access.
    # For "ACME Aurora Market", the search matches: "ACME Aurora Market" and "ACME Desert Cove Market"
    assert number_of_organizations_after_search == 2, f"Number of organizations after search is not 2, but {number_of_organizations_after_search}"  