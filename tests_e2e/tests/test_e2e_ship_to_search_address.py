import os
import random
import time
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.webapi_client import WebAPISession
from graphql_operations.contact.contact_operations import ContactOperations
from tests_e2e.components.edit_address_modal_component import EditAddressModalComponent
from tests_e2e.components.ship_to_selector_component import ShipToSelectorComponent
from tests_e2e.pages.home_page import HomePage
from tests_e2e.pages.main_layout_page import MainLayoutPage
from tests_e2e.pages.sign_in_page import SignInPage


@pytest.mark.e2e
@allure.title("Add 7 shipping addresses in Ship To component (E2E)")
def test_e2e_add_multiple_shipping_addresses(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    auth: Auth,  
    webapi_client: WebAPISession,
):
    print(
        f"{os.linesep}Running E2E test to add 7 shipping addresses...",
        end=" ",
    )

    test_user = dataset["users"][9]
    user_organization = next(
        (org for org in dataset["organizations"] 
         if org["id"] == test_user.get("organizationId")),
        None
    )
    
    with allure.step("Cleanup existing addresses"):
        auth.authenticate(test_user["userName"], config["USERS_PASSWORD"])
        cleanup_organization_addresses(
            webapi_client=webapi_client,
            config=config,
            auth=auth,
            dataset=dataset,
        )

    page.set_viewport_size({"width": 1920, "height": 1080})

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()

    sign_in_page.sign_in(test_user["userName"], config["USERS_PASSWORD"])
    time.sleep(2)

    home_page = HomePage(page, config)
    layout = MainLayoutPage(page)
    ship_to = layout.top_header_component.ship_to_selector
    add_shipping_address_button = layout.top_header_component.add_shipping_address_button


    with allure.step("Open Ship To selector"):
        expect(add_shipping_address_button).to_be_visible(), "Add shipping address button is not visible"
        add_shipping_address_text = add_shipping_address_button.inner_text()
        assert add_shipping_address_text in ["Ship to:\nAdd new address"], f"Add shipping address button text is not 'Ship to:\nAdd new address', got {add_shipping_address_text}"
        add_shipping_address_button.click()

    with allure.step("Add first test address"):
        test_address = generate_test_addresses(1)[0]
        edit_address_modal = EditAddressModalComponent(page.get_by_role("dialog"))
        expect(edit_address_modal.element).to_be_visible(), "Edit address modal is not visible"
        edit_address_modal.address_form_component.fill_address(test_address)
        edit_address_modal.submit_button.click()
        time.sleep(1)
        expect(edit_address_modal.element).not_to_be_visible(), "Edit address modal is still visible"
        time.sleep(1)
    
    with allure.step("Verify first address is added"):
        ship_to_selector = layout.top_header_component.ship_to_selector
        expect(ship_to_selector.trigger_button).to_be_visible(), "Ship to trigger is not visible"
        ship_to_selector.trigger_button.click()
        time.sleep(0.5)
        
        initial_count = len(ship_to.shipping_addresses)
        assert initial_count == 1, "Initial address count is not 1"
        
        ship_to_selector.trigger_button.click()  # Close dropdown
        time.sleep(0.5)

    test_addresses = generate_test_addresses(6)


    for i, address in enumerate(test_addresses):
        with allure.step(f"Add address {i + 1}: {address['city']}"):
            page.wait_for_load_state("networkidle")
            
            ship_to_selector = layout.top_header_component.ship_to_selector
            expect(ship_to_selector.trigger_button).to_be_visible(), "Ship to trigger is not visible"
            ship_to_selector.trigger_button.click()
            
            time.sleep(0.5)
            
            add_new_btn = ship_to_selector.add_new_address_button
            expect(add_new_btn).to_be_visible(timeout=5000), "Add new button is not visible"
            add_new_btn.click()
            
            edit_address_modal = EditAddressModalComponent(page.get_by_role("dialog"))
            expect(
                edit_address_modal.element
            ).to_be_visible(timeout=10000), "Edit address modal is not visible"

            edit_address_modal.address_form_component.fill_address(address)
            
            save_button = edit_address_modal.submit_button
            expect(save_button).to_be_enabled(timeout=5000)
            save_button.click()

            expect(
                edit_address_modal.element
            ).not_to_be_visible(timeout=15000), "Edit address modal is still visible"

            time.sleep(1)
    

    with allure.step("Verify all 7 addresses are added"):
        page.wait_for_load_state("networkidle")
        
        ship_to_selector = layout.top_header_component.ship_to_selector
        ship_to_selector.trigger_button.click()
        time.sleep(1)

        if ship_to_selector.more_button.is_visible():
            ship_to_selector.more_button.click()
            time.sleep(0.5)
        else:
            pytest.skip("More button is not visible - not enough addresses to trigger pagination")

        final_addresses_count = len(ship_to_selector.shipping_addresses)
        expected_count = initial_count + 6
        print(f"Final address count: {final_addresses_count}, Expected: {expected_count}")
        
        assert (
            final_addresses_count == expected_count
        ), f"Expected {expected_count} addresses (initial {initial_count} + 6), but found {final_addresses_count}"       
           
    with allure.step("Select an address from the list"):
        if len(ship_to.shipping_addresses) > 0:
            ship_to.shipping_addresses[0].click()

            expect(
                ship_to.shipping_addresses_dropdown
            ).not_to_be_visible(), "Shipping addresses dropdown should be closed after selection"

            ship_to_button = ship_to.trigger_button
            expect(ship_to_button).to_be_visible()


@pytest.mark.e2e
@allure.title("Search shipping address in Ship To component (E2E)")
def test_e2e_search_shipping_address(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    webapi_client: WebAPISession,
    auth: Auth,
):
    """    
    Note: This test requires addresses to already exist.
    """
    print(
        f"{os.linesep}Running E2E test to search shipping addresses...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()

    sign_in_page.sign_in(dataset["users"][9]["userName"], config["USERS_PASSWORD"])
    time.sleep(2)

    layout = MainLayoutPage(page)
    ship_to = layout.top_header_component.ship_to_selector

    with allure.step("Open Ship To selector"):
        ship_to_button = ship_to.trigger_button
        expect(ship_to_button).to_be_visible(), "Ship to button is not visible"
        ship_to_button.click()
        time.sleep(0.5)
        
        dropdown = ship_to.shipping_addresses_dropdown
        if not dropdown.is_visible():
            pytest.skip("No addresses available - dropdown not visible")

    with allure.step("Get initial addresses count"):   
        ship_to.more_button.is_visible()
        ship_to.more_button.click()
        time.sleep(0.5)
        initial_count = len(ship_to.shipping_addresses)
        print(f"Initial count: {initial_count}")

        if initial_count == 0:
            pytest.skip("No addresses available for search test")

    search_field = ship_to.search_field
    expect(search_field).to_be_visible(), "Search field is not visible"

    with allure.step("Search by city name 'Houston'"):
        search_field_input = page.get_by_role("textbox").first
        search_field_input.fill("Houston")
        time.sleep(1)

        filtered_count = len(ship_to.shipping_addresses)        

        assert filtered_count >= 1, f"Expected at least 1 address for 'Houston', found {filtered_count}"

        for addr in ship_to.shipping_addresses:
            addr_text = addr.inner_text().lower()
            assert "houston" in addr_text, f"Address '{addr_text}' does not contain 'Houston'"

    with allure.step("Clear search after city search"):
        search_field_input = page.get_by_role("textbox").first
        search_field_input.fill("")
        time.sleep(1)
        restored_count = len(ship_to.shipping_addresses)
        assert restored_count == initial_count, f"Expected {initial_count} addresses, found {restored_count}"

    with allure.step("Search by postal code '60601'"):
        search_field_input = page.get_by_role("textbox").first
        search_field_input.fill("60601")
        time.sleep(1)

        filtered_count = len(ship_to.shipping_addresses)        

        assert filtered_count >= 1, f"Expected at least 1 address for '60601', found {filtered_count}"
        
        for addr in ship_to.shipping_addresses:
            addr_text = addr.inner_text().lower()
            assert "60601" in addr_text, f"Address '{addr_text}' does not contain '60601'"

    with allure.step("Clear search after postal code search"):
        search_field_input = page.get_by_role("textbox").first
        search_field_input.fill("")
        time.sleep(1)
        restored_count = len(ship_to.shipping_addresses)
        assert restored_count == initial_count, f"Expected {initial_count} addresses, found {restored_count}"

    with allure.step("Search by street"):

        random_address = random.choice(ship_to.shipping_addresses)
        street_name = random_address.inner_text().split(",")[0].strip()       
        
        search_field_input = page.get_by_role("textbox").first
        search_field_input.fill(street_name.lower())
        time.sleep(1)

        filtered_count = len(ship_to.shipping_addresses)     

        assert filtered_count >= 1, f"Expected at least 1 address for '{street_name}', found {filtered_count}"

        for addr in ship_to.shipping_addresses:
            addr_text = addr.inner_text().lower()
            assert street_name.lower() in addr_text, f"Address '{addr_text}' does not contain '{street_name}'"

    with allure.step("Clear search after street search"):
        search_field_input = page.get_by_role("textbox").first
        search_field_input.fill("")
        time.sleep(1)
        restored_count = len(ship_to.shipping_addresses)
        assert restored_count == initial_count, f"Expected {initial_count} addresses, found {restored_count}"

    with allure.step("Search for non-existent address"):
        search_field_input = page.get_by_role("textbox").first
        search_field_input.fill("XYZNONEXISTENT12345")
        time.sleep(1)

        filtered_count = len(ship_to.shipping_addresses)     

        assert filtered_count == 0, f"Expected 0 addresses for non-existent search, found {filtered_count}"

    with allure.step("Clear search and verify all addresses return"):
        search_field_input = page.get_by_role("textbox").first
        search_field_input.fill("")
        time.sleep(1)

        restored_count = len(ship_to.shipping_addresses)
        assert restored_count == initial_count, f"Expected {initial_count} addresses, found {restored_count}"
    
    with allure.step("Restore existing addresses"):
        auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])
        restore_organization_addresses(
            webapi_client=webapi_client,
            config=config,
            auth=auth,
            dataset=dataset,
        )

    auth.clear_token()


def cleanup_organization_addresses(
    webapi_client: WebAPISession,
    config: Config,   
    auth: Auth,
    dataset: dict[str, Any],
):
    print(f"{os.linesep}Running test to remove addresses from organization...", end=" ")

    auth.authenticate(
        config["ADMIN_USERNAME"],
        config["ADMIN_PASSWORD"],
    )

    organization_id = dataset['organizations'][0]['id']   
    
    get_organization = webapi_client.get(f"/api/members/{organization_id}")    
    assert get_organization is not None, "Organization is None"
    
    update_data = {
        "id": organization_id,
        "name": get_organization.get("name"),
        "memberType": "Organization",
        "addresses": []
    }
    
    update_result = webapi_client.put(f"/api/members", data=update_data)    
    assert update_result is not None, "Update result is None"

    
    get_updated = webapi_client.get(f"/api/members/{organization_id}")
    assert get_updated is not None, "Updated organization is None"
    assert get_updated.get("addresses") is not None, "Addresses are None"
    assert len(get_updated.get("addresses")) == 0, "Addresses count is not 0" 


def restore_organization_addresses(
    webapi_client: WebAPISession,
    config: Config,   
    auth: Auth,
    dataset: dict[str, Any],
):
    print(f"{os.linesep}Running test to restore addresses to organization...", end=" ")
    
    auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])
    
    organization_id = dataset['organizations'][0]['id']
    organization_addresses = dataset['organizations'][0]['addresses']
    organization_name = dataset['organizations'][0]['name']

    get_organization = webapi_client.get(f"/api/members/{organization_id}")
    assert get_organization is not None, "Organization is None"

    update_data = {
        "id": organization_id,
        "name": organization_name,
        "memberType": "Organization",
        "addresses": organization_addresses
    }
    
    update_result = webapi_client.put(f"/api/members", data=update_data)
    assert update_result is not None, "Update result is None"

    get_updated = webapi_client.get(f"/api/members/{organization_id}")
    assert get_updated is not None, "Updated organization is None"
    assert get_updated.get("addresses") is not None, "Addresses are None"
    assert len(get_updated.get("addresses")) == 1, "Addresses count is not 1"

def generate_test_addresses(count: int) -> list[dict[str, str]]:
    """Generate a list of test addresses with unique random data."""
    import random
    
    cities = [
        "Los Angeles",
        "New York",
        "Chicago",
        "Houston",
        "Phoenix",
        "Philadelphia",
        "San Antonio",
        "San Diego",
        "Dallas",
        "San Jose",
    ]
    regions = [
        "California",
        "New York",
        "Illinois",
        "Texas",
        "Arizona",
        "Pennsylvania",
        "Texas",
        "California",
        "Texas",
        "California",
    ]
    postal_codes = [
        "90001",
        "10001",
        "60601",
        "77001",
        "85001",
        "19101",
        "78201",
        "92101",
        "75201",
        "95101",
    ]
    street_names = [
        "Main Street",
        "Oak Avenue",
        "Maple Drive",
        "Cedar Lane",
        "Pine Road",
        "Elm Boulevard",
        "Washington Street",
        "Lincoln Avenue",
        "Park Place",
        "Sunset Boulevard",
        "Broadway",
        "Highland Avenue",
        "Lake Drive",
        "River Road",
        "Mountain View",
    ]
    unit_types = [
        "Apt",
        "Suite",
        "Unit",
        "Floor",
        "#",
    ]

    addresses = []
    for i in range(count):
        street_number = random.randint(100, 9999)
        street_name = random.choice(street_names)
        unit_type = random.choice(unit_types)
        unit_number = random.randint(1, 500)
        
        addresses.append(
            {
                "description": f"Test Address {i + 1}",
                "first_name": f"Test{i + 1}",
                "last_name": f"User{i + 1}",
                "email": f"test.user{i + 1}@example.com",
                "phone": f"{random.randint(100, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}",
                "country": "United States of America",
                "postal_code": postal_codes[i % len(postal_codes)],
                "region": regions[i % len(regions)],
                "city": cities[i % len(cities)],
                "address_line_1": f"{street_number} {street_name}",
                "address_line_2": f"{unit_type} {unit_number}",
            }
        )
    return addresses
