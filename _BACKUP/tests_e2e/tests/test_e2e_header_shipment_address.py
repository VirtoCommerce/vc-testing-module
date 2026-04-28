import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config
from tests_e2e.components.edit_address_modal_component import EditAddressModalComponent
from tests_e2e.pages.home_page import HomePage

test_address = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "1234567890",
    "country": "United States of America",
    "postal_code": "12345",
    "region": "California",
    "city": "Los Angeles",
    "address_line_1": "123 Main St",
    "address_line_2": "Apt 1",
}


@pytest.mark.e2e
def test_e2e_add_shipment_address_in_header_for_anonymous_user(
    config: Config,
    page: Page,
):
    print(
        f"{os.linesep}Running E2E test to add shipment address in header for anonymous user...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    home_page = HomePage(page, config)
    home_page.navigate()

    expect(
        home_page.top_header_component.ship_to_selector.element
    ).not_to_be_visible(), "Ship to selector is visible"
    expect(
        home_page.top_header_component.add_shipping_address_button
    ).to_be_visible(), "Add shipping address button is not visible"

    home_page.top_header_component.add_shipping_address_button.click()

    edit_address_modal = EditAddressModalComponent(
        page.locator("[data-test-id='edit-address-modal']")
    )
    expect(
        edit_address_modal.element
    ).to_be_visible(), "Edit address modal is not visible"

    edit_address_modal.address_form_component.fill_address(test_address)
    edit_address_modal.submit_button.click()

    expect(
        home_page.top_header_component.ship_to_selector.element
    ).to_be_visible(), "Ship to selector is not visible"
    expect(
        home_page.top_header_component.ship_to_selector.selected_address_label
    ).to_be_visible(), "Ship to address label is not visible"
    expect(
        home_page.top_header_component.ship_to_selector.selected_address_label
    ).not_to_be_empty(), "Ship to address label is empty"
    expect(
        home_page.top_header_component.add_shipping_address_button
    ).not_to_be_visible(), "Add shipping address button is visible"


@pytest.mark.e2e
def test_e2e_select_shipment_address_in_header_for_registered_user(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    page: Page,
):
    print(
        f"{os.linesep}Running E2E test to add shipment address in header for anonymous user...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    home_page = HomePage(page, config)
    home_page.navigate()

    expect(
        home_page.top_header_component.ship_to_selector.element
    ).to_be_visible(), "Ship to selector is not visible"

    home_page.top_header_component.ship_to_selector.element.click()

    expect(
        home_page.top_header_component.ship_to_selector.shipping_addresses_dropdown
    ).to_be_visible(), "Shipping addresses dropdown is not visible"

    home_page.top_header_component.ship_to_selector.shipping_addresses[0].click()

    expect(
        home_page.top_header_component.ship_to_selector.shipping_addresses_dropdown
    ).not_to_be_visible(), "Shipping addresses dropdown is visible"
