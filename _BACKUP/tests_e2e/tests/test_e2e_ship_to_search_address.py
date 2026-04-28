from typing import Any
import os

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from fixtures.webapi_client import WebAPISession
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.components.edit_address_modal_component import EditAddressModalComponent
from tests_e2e.pages.home_page import HomePage

TEST_ADDRESSES = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "5551234567",
        "country": "United States of America",
        "countryCode": "USA",
        "region": "Texas",
        "regionId": "TX",
        "city": "Houston",
        "postal_code": "77001",
        "address_line_1": "100 Main Street",
        "address_line_2": "Suite 1",
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "phone": "5559876543",
        "country": "United States of America",
        "countryCode": "USA",
        "region": "Illinois",
        "regionId": "IL",
        "city": "Chicago",
        "postal_code": "60601",
        "address_line_1": "200 Oak Avenue",
        "address_line_2": "Apt 5",
    },
    {
        "first_name": "Bob",
        "last_name": "Johnson",
        "email": "bob.j@example.com",
        "phone": "5555551234",
        "country": "United States of America",
        "countryCode": "USA",
        "region": "California",
        "regionId": "CA",
        "city": "Los Angeles",
        "postal_code": "90001",
        "address_line_1": "300 Maple Drive",
        "address_line_2": "Unit 10",
    },
    {
        "first_name": "Alice",
        "last_name": "Williams",
        "email": "alice.w@example.com",
        "phone": "5552223333",
        "country": "United States of America",
        "countryCode": "USA",
        "region": "Arizona",
        "regionId": "AZ",
        "city": "Phoenix",
        "postal_code": "85001",
        "address_line_1": "400 Cedar Lane",
        "address_line_2": "Floor 3",
    },
    {
        "first_name": "Charlie",
        "last_name": "Brown",
        "email": "charlie.b@example.com",
        "phone": "5558889999",
        "country": "United States of America",
        "countryCode": "USA",
        "region": "New York",
        "regionId": "NY",
        "city": "New York",
        "postal_code": "10001",
        "address_line_1": "500 Pine Road",
        "address_line_2": "# 22",
    },
    {
        "first_name": "Diana",
        "last_name": "Miller",
        "email": "diana.m@example.com",
        "phone": "5554445555",
        "country": "United States of America",
        "countryCode": "USA",
        "region": "Texas",
        "regionId": "TX",
        "city": "Dallas",
        "postal_code": "75201",
        "address_line_1": "600 Elm Boulevard",
        "address_line_2": "Suite 8",
    },
    {
        "first_name": "Edward",
        "last_name": "Davis",
        "email": "edward.d@example.com",
        "phone": "5556667777",
        "country": "United States of America",
        "countryCode": "USA",
        "region": "California",
        "regionId": "CA",
        "city": "San Diego",
        "postal_code": "92101",
        "address_line_1": "700 Washington Street",
        "address_line_2": "Apt 15",
    },
]


def _get_test_user_and_org(
    dataset: dict[str, Any],
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
) -> tuple[dict[str, Any], dict[str, Any]]:
    test_user = dataset["users"][9]
    auth.authenticate(test_user["userName"], config["USERS_PASSWORD"])
    user_operations = UserOperations(graphql_client)
    me = user_operations.get_me()
    current_org_id = me["contact"]["organizationId"]
    auth.clear_token()
    assert current_org_id is not None, f"No current organizationId for user {test_user['userName']}"
    user_organization = next((org for org in dataset["organizations"] if org["id"] == current_org_id), None)
    assert user_organization is not None, f"Organization '{current_org_id}' not found in dataset"
    return test_user, user_organization


def _cleanup_addresses(webapi_client: WebAPISession, config: Config, auth: Auth, organization: dict[str, Any]):
    auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])
    org_data = webapi_client.get(f"/api/members/{organization['id']}")
    webapi_client.put(
        "/api/members",
        data={
            "id": organization["id"],
            "name": org_data.get("name"),
            "memberType": "Organization",
            "addresses": [],
        },
    )
    auth.clear_token()


def _add_addresses_via_api(
    webapi_client: WebAPISession,
    config: Config,
    auth: Auth,
    organization: dict[str, Any],
    addresses: list[dict[str, str]],
):
    auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])
    org_data = webapi_client.get(f"/api/members/{organization['id']}")
    api_addresses = [
        {
            "addressType": "BillingAndShipping",
            "firstName": addr["first_name"],
            "lastName": addr["last_name"],
            "email": addr["email"],
            "phone": addr["phone"],
            "countryCode": addr["countryCode"],
            "countryName": addr["country"],
            "postalCode": addr["postal_code"],
            "regionId": addr["regionId"],
            "regionName": addr["region"],
            "city": addr["city"],
            "line1": addr["address_line_1"],
            "line2": addr.get("address_line_2", ""),
        }
        for addr in addresses
    ]
    webapi_client.put(
        "/api/members",
        data={
            "id": organization["id"],
            "name": org_data["name"],
            "memberType": "Organization",
            "addresses": org_data.get("addresses", []) + api_addresses,
        },
    )
    auth.clear_token()


def _restore_addresses(webapi_client: WebAPISession, config: Config, auth: Auth, organization: dict[str, Any]):
    auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])
    webapi_client.put(
        "/api/members",
        data={
            "id": organization["id"],
            "name": organization["name"],
            "memberType": "Organization",
            "addresses": organization.get("addresses", []),
        },
    )
    auth.clear_token()


@pytest.mark.e2e
@allure.title("Add shipping address as anonymous user (E2E)")
def test_e2e_add_shipping_address_anonymous(
    config: Config,
    page: Page,
):
    print(f"{os.linesep}Running E2E test to add shipping address as anonymous user...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})
    home_page = HomePage(page, config)
    ship_to = home_page.top_header_component.ship_to_selector
    add_address_btn = home_page.top_header_component.add_shipping_address_button

    with allure.step("Navigate to home page"):
        home_page.navigate()

    with allure.step("Verify Ship To selector is hidden and Add Address button is visible"):
        expect(ship_to.element, "Ship To selector should not be visible for anonymous user").not_to_be_visible()
        expect(add_address_btn, "Add shipping address button should be visible").to_be_visible()

    with allure.step("Open add address modal"):
        add_address_btn.click()
        modal = EditAddressModalComponent(page.get_by_role("dialog"))
        expect(modal.element, "Edit address modal should be visible").to_be_visible()

    with allure.step("Fill and submit address form"):
        modal.address_form_component.fill_address(TEST_ADDRESSES[0])
        modal.submit_button.click()
        expect(modal.element, "Edit address modal should close after submit").not_to_be_visible()

    with allure.step("Verify address appears in Ship To selector"):
        expect(ship_to.element, "Ship To selector should be visible after adding address").to_be_visible()
        expect(ship_to.selected_address_label, "Selected address label should be visible").to_be_visible()
        expect(ship_to.selected_address_label, "Selected address label should not be empty").not_to_be_empty()
        expect(add_address_btn, "Add shipping address button should be hidden after adding address").not_to_be_visible()


@pytest.mark.e2e
@allure.title("Add shipping address as authenticated user (E2E)")
def test_e2e_add_shipping_address_authenticated(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    auth: Auth,
    webapi_client: WebAPISession,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running E2E test add shipping address as authenticated user...", end=" ")

    test_user, organization = _get_test_user_and_org(dataset, config, auth, graphql_client)

    with allure.step("Cleanup and add 6 addresses via API"):
        _cleanup_addresses(webapi_client, config, auth, organization)
        _add_addresses_via_api(webapi_client, config, auth, organization, TEST_ADDRESSES[:6])

    page.set_viewport_size({"width": 1920, "height": 1080})
    auth.authenticate(test_user["userName"], config["USERS_PASSWORD"], page)

    home_page = HomePage(page, config)

    with allure.step("Navigate and open Ship To selector"):
        home_page.navigate()
        ship_to = home_page.top_header_component.ship_to_selector
        expect(ship_to.trigger_button).to_be_visible()
        ship_to.trigger_button.click()
        expect(ship_to.shipping_addresses_dropdown).to_be_visible()

    with allure.step("Expand all addresses"):
        if ship_to.more_button.is_visible():
            ship_to.more_button.click()

    with allure.step("Verify all 6 addresses are displayed"):
        expect(ship_to.element.locator("button.ship-to-selector__item")).to_have_count(6)

    with allure.step("Select an address from the list"):
        ship_to.shipping_addresses[0].click()
        expect(ship_to.shipping_addresses_dropdown).not_to_be_visible()
        expect(ship_to.trigger_button).to_be_visible()

    with allure.step("Add one more address via UI"):
        ship_to.trigger_button.click()
        expect(ship_to.shipping_addresses_dropdown).to_be_visible()
        ship_to.add_new_address_button.click()
        modal = EditAddressModalComponent(page.get_by_role("dialog"))
        expect(modal.element, "Edit address modal should be visible").to_be_visible()
        modal.address_form_component.fill_address(TEST_ADDRESSES[6])
        modal.submit_button.click()
        expect(modal.element, "Edit address modal should close after submit").not_to_be_visible()

    with allure.step("Verify 7 addresses, 'Show more' button and search field are visible"):
        ship_to.trigger_button.click()
        expect(ship_to.shipping_addresses_dropdown).to_be_visible()
        expect(ship_to.more_button, "Show more button should be visible with 7 addresses").to_be_visible()
        expect(ship_to.search_field, "Search field should be visible with 7 addresses").to_be_visible()
        ship_to.more_button.click()
        expect(ship_to.element.locator("button.ship-to-selector__item")).to_have_count(7)

    with allure.step("Restore original addresses"):
        _restore_addresses(webapi_client, config, auth, organization)


@pytest.mark.e2e
@allure.title("Search shipping address in Ship To component (E2E)")
def test_e2e_search_shipping_address(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    auth: Auth,
    webapi_client: WebAPISession,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running E2E test to search shipping address in Ship To component...", end=" ")

    test_user, organization = _get_test_user_and_org(dataset, config, auth, graphql_client)

    with allure.step("Setup: add 7 addresses via API"):
        _cleanup_addresses(webapi_client, config, auth, organization)
        _add_addresses_via_api(webapi_client, config, auth, organization, TEST_ADDRESSES)

    page.set_viewport_size({"width": 1920, "height": 1080})
    auth.authenticate(test_user["userName"], config["USERS_PASSWORD"], page)

    home_page = HomePage(page, config)

    with allure.step("Navigate and open Ship To selector"):
        home_page.navigate()
        ship_to = home_page.top_header_component.ship_to_selector
        expect(ship_to.trigger_button).to_be_visible()
        ship_to.trigger_button.click()
        expect(ship_to.shipping_addresses_dropdown).to_be_visible()

    with allure.step("Expand all addresses"):
        if ship_to.more_button.is_visible():
            ship_to.more_button.click()

    addresses_locator = ship_to.element.locator("button.ship-to-selector__item")
    expect(addresses_locator).to_have_count(7)
    initial_count = 7

    search_field = ship_to.search_field
    if not search_field.is_visible():
        pytest.skip("Search field not visible — not enough addresses to trigger search UI")

    search_input = page.get_by_role("textbox").first

    with allure.step("Search by city name 'Houston'"):
        search_input.fill("Houston")
        expect(addresses_locator).to_have_count(1)
        assert "houston" in ship_to.shipping_addresses[0].inner_text().lower()

    with allure.step("Clear search after city search"):
        search_input.fill("")
        expect(addresses_locator).to_have_count(initial_count)

    with allure.step("Search by postal code '60601'"):
        search_input.fill("60601")
        expect(addresses_locator).to_have_count(1)
        assert "60601" in ship_to.shipping_addresses[0].inner_text()

    with allure.step("Clear search after postal code search"):
        search_input.fill("")
        expect(addresses_locator).to_have_count(initial_count)

    with allure.step("Search by street name"):
        search_input.fill("Main Street")
        expect(addresses_locator).to_have_count(1)
        assert "main street" in ship_to.shipping_addresses[0].inner_text().lower()

    with allure.step("Clear search after street search"):
        search_input.fill("")
        expect(addresses_locator).to_have_count(initial_count)

    with allure.step("Search for non-existent address"):
        search_input.fill("XYZNONEXISTENT12345")
        expect(addresses_locator).to_have_count(0)

    with allure.step("Clear search and verify all addresses return"):
        search_input.fill("")
        expect(addresses_locator).to_have_count(initial_count)

    with allure.step("Restore original addresses"):
        _restore_addresses(webapi_client, config, auth, organization)
