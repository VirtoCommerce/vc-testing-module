"""
E2E tests for the pickup locations modal on the product page.

Test Cases:
- test_e2e_product_pickup_locations_modal_elements: Verify modal opens and all key UI elements are displayed
- test_e2e_product_pickup_locations_list_content: Verify locations list contains items with name, address, and availability
- test_e2e_product_pickup_locations_search_found: Search for a keyword that returns results
- test_e2e_product_pickup_locations_search_not_found: Search for a keyword that returns no results
- test_e2e_product_pickup_locations_reset_search: Search, then reset and verify full list is restored
- test_e2e_product_pickup_locations_reset_search_button: Search non-existent keyword, click Reset search button to restore list
- test_e2e_product_pickup_locations_select_location: Click a location to open the card dialog and verify content
- test_e2e_product_pickup_locations_close_modal: Close the modal using the close button
"""

import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures import Config
from tests_e2e.helpers import build_seo_path
from tests_e2e.pages import ProductPage

PRODUCT_ID = "product-acme-laptop-asus-vivobook-16-x1607qa"
SEARCH_KEYWORD = "Union Square Greenmarket"


@pytest.fixture
def product_page(page: Page, config: Config, dataset: dict[str, Any]) -> ProductPage:
    """Navigate to the pickup locations test product page."""
    page.set_viewport_size({"width": 1920, "height": 1080})
    product = next(p for p in dataset["products"] if p["id"] == PRODUCT_ID)
    pp = ProductPage(page, config, build_seo_path(product, dataset))
    pp.navigate()
    return pp


@pytest.mark.e2e
@allure.title("Verify pickup locations modal elements on product page (E2E)")
def test_e2e_product_pickup_locations_modal_elements(
    page: Page,
    product_page: ProductPage,
):
    print(
        f"{os.linesep}Running E2E test to verify pickup locations modal elements on product page...",
        end=" ",
    )

    expect(
        product_page.shipment_options_widget,
        "Shipment options widget should be visible on product page",
    ).to_be_visible()

    expect(
        product_page.check_pickup_locations_button,
        "Check pickup locations button should be visible on product page",
    ).to_be_visible()

    modal = product_page.open_pickup_locations_modal()

    expect(modal.element, "Pickup locations modal should be visible").to_be_visible()
    expect(modal.search_keyword_input, "Search input should be visible in modal").to_be_visible()
    expect(modal.search_button, "Search button should be visible in modal").to_be_visible()
    expect(modal.pickup_locations_list, "Pickup locations list should be visible in modal").to_be_visible()
    expect(modal.pickup_locations_map, "Google Map should be visible in modal").to_be_visible()
    expect(modal.select_address_map_desktop, "Desktop layout container should be visible in modal").to_be_visible()
    expect(modal.close_button, "Close button should be visible in modal").to_be_visible()

    assert modal.pickup_location_items.count() > 0, "At least one pickup location item should be displayed"


@pytest.mark.e2e
@allure.title("Verify pickup locations list content on product page (E2E)")
def test_e2e_product_pickup_locations_list_content(
    page: Page,
    product_page: ProductPage,
):
    print(
        f"{os.linesep}Running E2E test to verify pickup locations list content on product page...",
        end=" ",
    )

    modal = product_page.open_pickup_locations_modal()

    expect(modal.pickup_locations_list, "Pickup locations list should be visible").to_be_visible()

    total_locations_count = modal.pickup_location_items.count()
    assert total_locations_count > 0, f"Expected at least one pickup location, got {total_locations_count}"

    first_name = modal.get_location_name_by_index(0)
    first_address = modal.get_location_address_by_index(0)
    first_chip = modal.get_availability_chip_by_index(0)

    expect(first_name, "First location name should be visible").to_be_visible()
    expect(first_address, "First location address should be visible").to_be_visible()
    expect(first_chip, "First location availability chip should be visible").to_be_visible()

    first_name_text = first_name.text_content()
    first_address_text = first_address.text_content()
    first_chip_text = first_chip.text_content()

    assert first_name_text and len(first_name_text.strip()) > 0, "First location name should not be empty"
    assert first_address_text and len(first_address_text.strip()) > 0, "First location address should not be empty"
    assert first_chip_text and first_chip_text.strip() in (
        "Today",
        "Via transfer",
    ), f"Availability chip should be 'Today' or 'Via transfer', got '{first_chip_text}'"

    names_count = modal.pickup_location_names.count()
    addresses_count = modal.pickup_location_addresses.count()
    chips_count = modal.pickup_availability_chips.count()

    assert (
        names_count == total_locations_count
    ), f"All locations should have names, expected {total_locations_count}, got {names_count}"
    assert (
        addresses_count == total_locations_count
    ), f"All locations should have addresses, expected {total_locations_count}, got {addresses_count}"
    assert (
        chips_count == total_locations_count
    ), f"All locations should have availability chips, expected {total_locations_count}, got {chips_count}"


@pytest.mark.e2e
@allure.title("Search pickup locations with matching keyword on product page (E2E)")
def test_e2e_product_pickup_locations_search_found(
    page: Page,
    product_page: ProductPage,
):
    print(
        f"{os.linesep}Running E2E test to search pickup locations with matching keyword on product page...",
        end=" ",
    )

    modal = product_page.open_pickup_locations_modal()

    expect(modal.pickup_locations_list, "Pickup locations list should be visible").to_be_visible()

    initial_count = modal.pickup_location_items.count()

    keyword_to_search = SEARCH_KEYWORD

    modal.search(keyword_to_search)

    expect(modal.pickup_location_items.first, "At least one filtered result should be visible").to_be_visible()
    expect(
        modal.pickup_location_items,
        f"Filtered results should be fewer than total ({initial_count})",
    ).not_to_have_count(initial_count, timeout=10_000)

    filtered_count = modal.pickup_location_items.count()
    assert filtered_count >= 1, f"At least one location should match the keyword '{keyword_to_search}'"
    assert (
        filtered_count < initial_count
    ), f"Filtered results ({filtered_count}) should be fewer than total ({initial_count})"

    expect(
        modal.pickup_locations_not_found,
        "Not found message should not be visible when results exist",
    ).not_to_be_visible()

    for i in range(filtered_count):
        name_text = modal.get_location_name_by_index(i).text_content() or ""
        address_text = modal.get_location_address_by_index(i).text_content() or ""
        combined_text = f"{name_text} {address_text}".lower()
        assert keyword_to_search.lower() in combined_text, (
            f"Location at index {i} (name='{name_text}', address='{address_text}') "
            f"does not contain keyword '{keyword_to_search}'"
        )


@pytest.mark.e2e
@allure.title("Search pickup locations with non-matching keyword on product page (E2E)")
def test_e2e_product_pickup_locations_search_not_found(
    page: Page,
    product_page: ProductPage,
):
    print(
        f"{os.linesep}Running E2E test to search pickup locations with non-matching keyword on product page...",
        end=" ",
    )

    modal = product_page.open_pickup_locations_modal()

    expect(modal.pickup_locations_list, "Pickup locations list should be visible").to_be_visible()

    keyword_to_search = "NonExistentLocationXYZ123"

    modal.search(keyword_to_search)

    expect(
        modal.pickup_locations_not_found,
        "Not found message should be visible when no locations match the search",
    ).to_be_visible()

    assert (
        modal.pickup_location_items.count() == 0
    ), f"No pickup locations should be displayed for keyword '{keyword_to_search}'"


@pytest.mark.e2e
@allure.title("Reset search and restore full pickup locations list on product page (E2E)")
def test_e2e_product_pickup_locations_reset_search(
    page: Page,
    product_page: ProductPage,
):
    print(
        f"{os.linesep}Running E2E test to reset search and restore pickup locations list on product page...",
        end=" ",
    )

    modal = product_page.open_pickup_locations_modal()

    expect(modal.pickup_locations_list, "Pickup locations list should be visible").to_be_visible()

    initial_count = modal.pickup_location_items.count()
    assert initial_count > 0, f"Expected at least one pickup location initially, got {initial_count}"

    # Search to filter the list
    keyword_to_search = SEARCH_KEYWORD
    modal.search(keyword_to_search)

    # Wait for the list to actually filter
    expect(
        modal.pickup_location_items,
        f"Filtered results should be fewer than total ({initial_count})",
    ).not_to_have_count(initial_count, timeout=10_000)

    filtered_count = modal.pickup_location_items.count()
    assert (
        filtered_count < initial_count
    ), f"Filtered count ({filtered_count}) should be less than initial count ({initial_count})"

    # Reset the search by clearing input and pressing Enter
    modal.clear_search()

    # Wait for the full list to be restored
    expect(modal.pickup_location_items.first, "First location item should be visible after reset").to_be_visible()
    expect(
        modal.pickup_location_items,
        f"Full list should be restored to {initial_count} items",
    ).to_have_count(initial_count, timeout=10_000)

    restored_count = modal.pickup_location_items.count()
    assert (
        restored_count == initial_count
    ), f"After reset, expected {initial_count} pickup locations, got {restored_count}"

    # Verify the search input is cleared
    expect(modal.search_keyword_input, "Search input should be empty after reset").to_have_value("")


@pytest.mark.e2e
@allure.title("Reset search via reset button and restore full pickup locations list on product page (E2E)")
def test_e2e_product_pickup_locations_reset_search_button(
    page: Page,
    product_page: ProductPage,
):
    print(
        f"{os.linesep}Running E2E test to reset search via reset button on product page...",
        end=" ",
    )

    modal = product_page.open_pickup_locations_modal()

    expect(modal.pickup_locations_list, "Pickup locations list should be visible").to_be_visible()

    initial_count = modal.pickup_location_items.count()
    assert initial_count > 0, f"Expected at least one pickup location initially, got {initial_count}"

    # Search for a non-existent keyword to trigger "not found" state
    keyword_to_search = "NonExistentLocationXYZ123"
    modal.search(keyword_to_search)

    # Verify "not found" message and reset button are visible
    expect(
        modal.pickup_locations_not_found,
        "Not found message should be visible when no locations match the search",
    ).to_be_visible()
    assert modal.pickup_location_items.count() == 0, "No pickup locations should be displayed"

    expect(
        modal.reset_search_button,
        "Reset search button should be visible when no results found",
    ).to_be_visible()

    modal.reset_search_button.click()

    expect(modal.pickup_location_items.first, "First location item should be visible after reset").to_be_visible()
    expect(
        modal.pickup_location_items,
        f"Full list should be restored to {initial_count} items",
    ).to_have_count(initial_count, timeout=10_000)

    restored_count = modal.pickup_location_items.count()
    assert (
        restored_count == initial_count
    ), f"After reset, expected {initial_count} pickup locations, got {restored_count}"

    expect(modal.search_keyword_input, "Search input should be empty after reset").to_have_value("")

    expect(
        modal.pickup_locations_not_found,
        "Not found message should not be visible after reset",
    ).not_to_be_visible()
    expect(
        modal.reset_search_button,
        "Reset search button should not be visible after reset",
    ).not_to_be_visible()


@pytest.mark.e2e
@allure.title("Select a pickup location and verify card dialog on product page (E2E)")
def test_e2e_product_pickup_locations_select_location(
    page: Page,
    product_page: ProductPage,
):
    print(
        f"{os.linesep}Running E2E test to select a pickup location and verify card dialog on product page...",
        end=" ",
    )

    modal = product_page.open_pickup_locations_modal()

    expect(modal.pickup_locations_list, "Pickup locations list should be visible").to_be_visible()

    map_locator = modal.pickup_locations_map
    markers = map_locator.locator("gmp-advanced-marker")
    if markers.count() > 0:
        markers.first.wait_for(state="attached", timeout=15_000)
    else:
        map_locator.locator("button[aria-label]").first.wait_for(state="attached", timeout=15_000)

    total_count = modal.pickup_location_items.count()
    assert total_count >= 2, f"Expected at least 2 pickup locations, got {total_count}"

    # Select multiple locations: first, second, and last
    indices_to_test = [0, 1, total_count - 1]
    card = modal.pickup_location_card

    for index in indices_to_test:
        location_name_text = modal.get_location_name_by_index(index).text_content()
        modal.click_location_by_index(index)

        expect(card.element, f"Card should be visible after clicking location at index {index}").to_be_visible()
        expect(card.name, f"Card name should be visible for location at index {index}").to_be_visible()
        expect(card.info, f"Card info should be visible for location at index {index}").to_be_visible()

        card_name_text = card.name.text_content()
        assert (
            card_name_text == location_name_text
        ), f"Card name '{card_name_text}' should match clicked location name '{location_name_text}' at index {index}"

        card.close_button.click()

        expect(card.element, f"Card should be hidden after closing for location at index {index}").not_to_be_visible()

    expect(modal.element, "Pickup locations modal should still be visible after closing card dialog").to_be_visible()


@pytest.mark.e2e
@allure.title("Close pickup locations modal using close button on product page (E2E)")
def test_e2e_product_pickup_locations_close_modal(
    page: Page,
    product_page: ProductPage,
):
    print(
        f"{os.linesep}Running E2E test to close pickup locations modal on product page...",
        end=" ",
    )

    modal = product_page.open_pickup_locations_modal()

    expect(modal.element, "Pickup locations modal should be visible").to_be_visible()

    modal.close_button.click()

    expect(
        modal.element,
        "Pickup locations modal should not be visible after clicking close",
    ).not_to_be_visible()

    expect(
        product_page.check_pickup_locations_button,
        "Check pickup locations button should still be visible after closing modal",
    ).to_be_visible()
