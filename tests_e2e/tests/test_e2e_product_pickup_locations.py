"""
E2E tests for the pickup locations modal on the product page.

Test Cases:
- test_e2e_product_pickup_locations_modal_and_list: Verify modal UI elements and list content (name, address, availability)
- test_e2e_product_pickup_locations_search_found[full_name]: Search by exact full location name
- test_e2e_product_pickup_locations_search_found[partial_name]: Search by first word of a location name
- test_e2e_product_pickup_locations_search_found[city]: Search by city name (skipped — known frontend bug)
- test_e2e_product_pickup_locations_search_found[street]: Search by street address (skipped — known frontend bug)
- test_e2e_product_pickup_locations_search_found[postal_code]: Search by postal code (skipped — known frontend bug)
- test_e2e_product_pickup_locations_search_found[special_char]: Search by name containing special characters
- test_e2e_product_pickup_locations_search_found[whitespace]: Search with leading/trailing whitespace (skipped — UI does not trim)
- test_e2e_product_pickup_locations_search_reset: Search found → clear reset → search not found → reset button
- test_e2e_product_pickup_locations_select_location: Click locations to verify card dialog, then close modal
- test_e2e_product_out_of_stock_pickup_locations_not_displayed: Product out of stock — pickup locations widget is NOT displayed
"""

import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures import Config, GraphQLClient
from graphql_operations.pickup_locations.pickup_locations_operations import (
    PickupLocationsOperations,
)
from tests_e2e.helpers import build_seo_path, navigate_to_product_page, resolve_search_keyword
from tests_e2e.pages import ProductPage

PRODUCT_ID = "product-acme-laptop-asus-vivobook-16-x1607qa"
OUT_OF_STOCK_PRODUCT_ID = "product-acme-laptop-acer-aspire-16-ai"
NON_EXISTENT_KEYWORD = "NonExistentLocationXYZ123"


@pytest.fixture
def pickup_locations_data(graphql_client: GraphQLClient, config: Config, dataset: dict[str, Any]) -> dict[str, Any]:
    """Fetch product pickup locations via GraphQL to use as expected data in E2E tests."""
    operations = PickupLocationsOperations(graphql_client)
    culture = dataset["languages"][0]["allowedValues"][0]
    initial = operations.get_product_pickup_locations(
        product_id=PRODUCT_ID,
        store_id=config["STORE_ID"],
        culture_name=culture,
        first=50,
    )
    total = initial["totalCount"]
    assert total > 0, f"No pickup locations found for product {PRODUCT_ID} via GraphQL"

    result = operations.get_product_pickup_locations(
        product_id=PRODUCT_ID,
        store_id=config["STORE_ID"],
        culture_name=culture,
        first=total,
    )
    return result


@pytest.fixture
def product_page(page: Page, config: Config, dataset: dict[str, Any]) -> ProductPage:
    """Navigate to the pickup locations test product page."""
    return navigate_to_product_page(page, config, dataset, PRODUCT_ID)


@pytest.mark.e2e
@allure.title("Verify pickup locations modal and list content on product page (E2E)")
def test_e2e_product_pickup_locations_modal_and_list(
    product_page: ProductPage,
    pickup_locations_data: dict[str, Any],
):
    print(
        f"{os.linesep}Running E2E test to verify pickup locations modal and list content on product page...",
        end=" ",
    )

    expected_count = pickup_locations_data["totalCount"]
    expected_names = {loc["name"] for loc in pickup_locations_data["items"]}

    with allure.step("Verify product page elements"):
        expect(
            product_page.shipment_options_widget,
            "Shipment options widget should be visible on product page",
        ).to_be_visible()

        expect(
            product_page.check_pickup_locations_button,
            "Check pickup locations button should be visible on product page",
        ).to_be_visible()

    modal = product_page.open_pickup_locations_modal()
    modal.wait_for_map_ready()

    with allure.step("Verify modal UI elements"):
        expect(modal.element, "Pickup locations modal should be visible").to_be_visible()
        expect(modal.search_keyword_input, "Search input should be visible in modal").to_be_visible()
        expect(modal.search_button, "Search button should be visible in modal").to_be_visible()
        expect(
            modal.pickup_locations_list,
            "Pickup locations list should be visible in modal",
        ).to_be_visible()
        expect(modal.pickup_locations_map, "Google Map should be visible in modal").to_be_visible()
        expect(
            modal.select_address_map_desktop,
            "Desktop layout container should be visible in modal",
        ).to_be_visible()
        expect(modal.close_button, "Close button should be visible in modal").to_be_visible()

    expect(
        modal.pickup_location_items,
        f"Pickup locations count should match GraphQL ({expected_count})",
    ).to_have_count(expected_count, timeout=10_000)

    with allure.step("Verify list content"):
        first_name = modal.get_location_name_by_index(0)
        first_address = modal.get_location_address_by_index(0)
        first_chip = modal.get_availability_chip_by_index(0)

        expect(first_name, "First location name should be visible").to_be_visible()
        expect(first_address, "First location address should be visible").to_be_visible()
        expect(first_chip, "First location availability chip should be visible").to_be_visible()

        first_name_text = (first_name.text_content() or "").strip()
        first_address_text = (first_address.text_content() or "").strip()
        first_chip_text = (first_chip.text_content() or "").strip()

        assert first_name_text, "First location name should not be empty"
        assert first_address_text, "First location address should not be empty"
        assert first_chip_text, "First location availability chip should not be empty"

        assert (
            first_name_text in expected_names
        ), f"First location name '{first_name_text}' should match one of the GraphQL names: {expected_names}"

        names_count = modal.pickup_location_names.count()
        addresses_count = modal.pickup_location_addresses.count()
        chips_count = modal.pickup_availability_chips.count()

        assert (
            names_count == expected_count
        ), f"All locations should have names, expected {expected_count}, got {names_count}"
        assert (
            addresses_count == expected_count
        ), f"All locations should have addresses, expected {expected_count}, got {addresses_count}"
        assert (
            chips_count == expected_count
        ), f"All locations should have availability chips, expected {expected_count}, got {chips_count}"


_ADDRESS_SEARCH_BUG_REASON = "Frontend search only matches by name, not by address fields (to be fixed by dev team)"
_WHITESPACE_SEARCH_BUG_REASON = "Frontend search does not trim leading/trailing whitespace (to be fixed by dev team)"

SEARCH_CASES = [
    pytest.param("full_name", id="full_name"),
    pytest.param("partial_name", id="partial_name"),
    pytest.param("city", id="city", marks=pytest.mark.skip(reason=_ADDRESS_SEARCH_BUG_REASON)),
    pytest.param(
        "street",
        id="street",
        marks=pytest.mark.skip(reason=_ADDRESS_SEARCH_BUG_REASON),
    ),
    pytest.param(
        "postal_code",
        id="postal_code",
        marks=pytest.mark.skip(reason=_ADDRESS_SEARCH_BUG_REASON),
    ),
    pytest.param("special_char", id="special_char"),
    pytest.param(
        "whitespace",
        id="whitespace",
        marks=pytest.mark.skip(reason=_WHITESPACE_SEARCH_BUG_REASON),
    ),
]


@pytest.mark.e2e
@pytest.mark.parametrize("search_case_id", SEARCH_CASES)
@allure.title("Search pickup locations on product page (E2E)")
def test_e2e_product_pickup_locations_search_found(
    product_page: ProductPage,
    pickup_locations_data: dict[str, Any],
    search_case_id: str,
):
    items = pickup_locations_data["items"]
    keyword_to_search = resolve_search_keyword(items, search_case_id)
    keyword_display = keyword_to_search.strip().encode("ascii", "replace").decode()
    allure.dynamic.title(f"Search pickup locations by {search_case_id}: '{keyword_to_search.strip()}' (E2E)")

    print(
        f"{os.linesep}Running E2E search test [{search_case_id}] keyword='{keyword_display}'...",
        end=" ",
    )

    expected_total = pickup_locations_data["totalCount"]

    modal = product_page.open_pickup_locations_modal()
    modal.wait_for_map_ready()

    expect(modal.pickup_locations_list, "Pickup locations list should be visible").to_be_visible()

    expect(
        modal.pickup_location_items,
        f"Initial count should match GraphQL ({expected_total})",
    ).to_have_count(expected_total, timeout=10_000)

    with allure.step(f"Search by '{keyword_display}' and verify filtered results"):
        modal.search(keyword_to_search)
        modal.wait_for_search_results()

        expect(
            modal.pickup_locations_not_found,
            "Not found message should not be visible when results exist",
        ).not_to_be_visible()

    filtered_count = modal.pickup_location_items.count()
    assert filtered_count > 0, f"At least one location should match keyword '{keyword_to_search.strip()}'"
    assert (
        filtered_count <= expected_total
    ), f"Search should not return more than total: got {filtered_count}, expected at most {expected_total}"

    with allure.step("Verify each filtered result contains the keyword"):
        keyword_normalized = keyword_to_search.strip().lower()
        for i in range(filtered_count):
            name_text = modal.get_location_name_by_index(i).text_content() or ""
            address_text = modal.get_location_address_by_index(i).text_content() or ""
            combined_text = f"{name_text} {address_text}".lower()
            assert keyword_normalized in combined_text, (
                f"[{search_case_id}] Location at index {i} (name='{name_text}', "
                f"address='{address_text}') does not contain keyword '{keyword_to_search.strip()}'"
            )

    with allure.step("Click first filtered location and verify card dialog"):
        first_name_text = (modal.get_location_name_by_index(0).text_content() or "").strip()
        modal.click_location_by_index(0)

        card = modal.pickup_location_card
        expect(card.element, "Card should be visible after clicking location").to_be_visible()
        expect(card.name, "Card name should be visible").to_be_visible()
        expect(card.info, "Card info should be visible").to_be_visible()

        card_name_text = (card.name.text_content() or "").strip()
        assert (
            card_name_text == first_name_text
        ), f"Card name '{card_name_text}' should match clicked location name '{first_name_text}'"

        card.close_button.click()
        expect(card.element, "Card should be hidden after closing").not_to_be_visible()


@pytest.mark.e2e
@allure.title("Search and reset pickup locations on product page (E2E)")
def test_e2e_product_pickup_locations_search_reset(
    product_page: ProductPage,
    pickup_locations_data: dict[str, Any],
):
    print(
        f"{os.linesep}Running E2E test to search and reset pickup locations on product page...",
        end=" ",
    )

    expected_total = pickup_locations_data["totalCount"]
    keyword_to_search = pickup_locations_data["items"][0]["name"]

    modal = product_page.open_pickup_locations_modal()
    modal.wait_for_map_ready()

    expect(modal.pickup_locations_list, "Pickup locations list should be visible").to_be_visible()

    expect(
        modal.pickup_location_items,
        f"Initial count should match GraphQL ({expected_total})",
    ).to_have_count(expected_total, timeout=10_000)

    with allure.step("Search with a valid keyword, then clear to restore the full list"):
        modal.search(keyword_to_search)

        expect(
            modal.pickup_location_items.first,
            "At least one filtered result should be visible",
        ).to_be_visible()

        modal.clear_search()

        expect(
            modal.pickup_location_items.first,
            "First location item should be visible after clear",
        ).to_be_visible()
        expect(
            modal.pickup_location_items,
            f"Full list should be restored to {expected_total} items after clear",
        ).to_have_count(expected_total, timeout=10_000)
        expect(modal.search_keyword_input, "Search input should be empty after clear").to_have_value("")

    with allure.step("Search with a non-existent keyword, then use Reset button to restore"):
        modal.search(NON_EXISTENT_KEYWORD)

        expect(
            modal.pickup_locations_not_found,
            "Not found message should be visible when no locations match the search",
        ).to_be_visible()
        assert (
            modal.pickup_location_items.count() == 0
        ), f"No pickup locations should be displayed for keyword '{NON_EXISTENT_KEYWORD}'"

        expect(
            modal.reset_search_button,
            "Reset search button should be visible when no results found",
        ).to_be_visible()

        modal.reset_search_button.click()

        expect(
            modal.pickup_location_items.first,
            "First location item should be visible after reset",
        ).to_be_visible()
        expect(
            modal.pickup_location_items,
            f"Full list should be restored to {expected_total} items after reset",
        ).to_have_count(expected_total, timeout=10_000)
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
    product_page: ProductPage,
    pickup_locations_data: dict[str, Any],
):
    print(
        f"{os.linesep}Running E2E test to select a pickup location and verify card dialog on product page...",
        end=" ",
    )

    expected_total = pickup_locations_data["totalCount"]
    expected_names = {loc["name"] for loc in pickup_locations_data["items"]}

    modal = product_page.open_pickup_locations_modal()
    modal.wait_for_map_ready()

    expect(modal.pickup_locations_list, "Pickup locations list should be visible").to_be_visible()

    expect(
        modal.pickup_location_items,
        f"Pickup locations count should match GraphQL ({expected_total})",
    ).to_have_count(expected_total, timeout=10_000)

    total_count = modal.pickup_location_items.count()
    assert total_count >= 2, f"Expected at least 2 pickup locations, got {total_count}"

    indices_to_test = sorted(set([0, 1, total_count - 1]))
    card = modal.pickup_location_card

    for index in indices_to_test:
        with allure.step(f"Click location at index {index} and verify card dialog"):
            location_name_text = modal.get_location_name_by_index(index).text_content()
            modal.click_location_by_index(index)

            expect(
                card.element,
                f"Card should be visible after clicking location at index {index}",
            ).to_be_visible()
            expect(card.name, f"Card name should be visible for location at index {index}").to_be_visible()
            expect(card.info, f"Card info should be visible for location at index {index}").to_be_visible()

            card_name_text = card.name.text_content()
            assert (
                card_name_text == location_name_text
            ), f"Card name '{card_name_text}' should match clicked location name '{location_name_text}' at index {index}"

            assert (
                card_name_text in expected_names
            ), f"Card name '{card_name_text}' should be one of the GraphQL location names: {expected_names}"

            card.close_button.click()

            expect(
                card.element,
                f"Card should be hidden after closing for location at index {index}",
            ).not_to_be_visible()

    with allure.step("Close modal and verify product page"):
        expect(
            modal.element,
            "Pickup locations modal should still be visible after closing card dialog",
        ).to_be_visible()

        modal.close_button.click()

        expect(
            modal.element,
            "Pickup locations modal should not be visible after clicking close",
        ).not_to_be_visible()

        expect(
            product_page.check_pickup_locations_button,
            "Check pickup locations button should still be visible after closing modal",
        ).to_be_visible()


@pytest.mark.e2e
@allure.title("Verify pickup locations widget is NOT displayed for out-of-stock product (E2E)")
def test_e2e_product_out_of_stock_pickup_locations_not_displayed(
    page: Page,
    config: Config,
    dataset: dict[str, Any],
):
    print(
        f"{os.linesep}Running E2E test to verify pickup locations widget is not displayed for out-of-stock product...",
        end=" ",
    )

    product_page = navigate_to_product_page(page, config, dataset, OUT_OF_STOCK_PRODUCT_ID)

    with allure.step("Verify product page loaded"):
        expect(
            product_page.product_name,
            "Product name should be visible on product page",
        ).to_be_visible()

    with allure.step("Verify pickup locations widget is NOT displayed for out-of-stock product"):
        expect(
            product_page.shipment_options_widget,
            "Shipment options widget should NOT be visible for out-of-stock product",
        ).not_to_be_visible()

        expect(
            product_page.check_pickup_locations_button,
            "Check pickup locations button should NOT be visible for out-of-stock product",
        ).not_to_be_visible()
