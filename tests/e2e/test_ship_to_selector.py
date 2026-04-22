import pytest
from core.global_settings import GlobalSettings
from page_objects.components import EditAddressModal
from page_objects.pages import HomePage
from playwright.sync_api import Page, expect
from tests.constants import TEST_ADDRESS

_USERNAME = "acme_store_employee_1@acme.com"


@pytest.mark.e2e
def test_ship_to_selector_anonymous_user(
    global_settings: GlobalSettings,
    page: Page,
) -> None:
    home_page = HomePage(global_settings=global_settings, page=page)
    home_page.navigate()

    expect(home_page.top_header.add_shipping_address_button).to_be_visible()

    home_page.top_header.add_shipping_address_button.click()

    edit_address_modal = EditAddressModal(root=page.locator("[data-test-id='edit-address-modal']"))
    expect(edit_address_modal.root).to_be_visible()

    edit_address_modal.address_form.fill(address=TEST_ADDRESS)
    edit_address_modal.submit_button.click()

    expect(home_page.top_header.add_shipping_address_button).not_to_be_visible()
    expect(home_page.top_header.ship_to_selector.selected_address_label).to_be_visible()
    expect(home_page.top_header.ship_to_selector.selected_address_label).to_contain_text(str(TEST_ADDRESS.city))
    expect(home_page.top_header.ship_to_selector.selected_address_label).to_contain_text(str(TEST_ADDRESS.country_name))
    expect(home_page.top_header.ship_to_selector.selected_address_label).to_contain_text(str(TEST_ADDRESS.region_name))
    expect(home_page.top_header.ship_to_selector.selected_address_label).to_contain_text(str(TEST_ADDRESS.city))
    expect(home_page.top_header.ship_to_selector.selected_address_label).to_contain_text(str(TEST_ADDRESS.postal_code))
    expect(home_page.top_header.ship_to_selector.selected_address_label).to_contain_text(str(TEST_ADDRESS.line1))


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
def test_ship_to_selector_registered_user(
    global_settings: GlobalSettings,
    page: Page,
) -> None:
    home_page = HomePage(global_settings=global_settings, page=page)
    home_page.navigate()

    expect(home_page.top_header.ship_to_selector.root).to_be_visible()

    home_page.top_header.ship_to_selector.root.click()
    expect(home_page.top_header.ship_to_selector.addresses_list).to_be_visible()

    home_page.top_header.ship_to_selector.addresses.nth(0).click()
    expect(home_page.top_header.ship_to_selector.selected_address_label).to_be_visible()
