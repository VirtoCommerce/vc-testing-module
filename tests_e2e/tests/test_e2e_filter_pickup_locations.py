import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.components.select_bopis_map_modal_component import (
    SelectBopisMapModalComponent,
)
from tests_e2e.pages import CartPage, CheckoutShippingPage


@pytest.mark.e2e
@pytest.mark.checkout_mode("single-page")
def test_e2e_filter_pickup_locations_elements_single_page_checkout(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to check filter pickup locations elements on pickup point selection modal in single-page checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    country_to_filter = "United States of America"
    region_to_filter = "New York"
    city_to_filter = "Manhattan"

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    product = dataset["products"][1]

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": 2,
        }
    )

    cart_page = CartPage(config, page)
    cart_page.navigate()

    cart_page.shipping_details_section_component.pickup_delivery_option_switcher.click()
    cart_page.shipping_details_section_component.pickup_point_section.locator(
        "[data-test-id='select-address-button']"
    ).click()

    select_pickup_location_modal = SelectBopisMapModalComponent(page.locator(".select-address-map-modal"))

    expect(select_pickup_location_modal.element).to_be_visible()
    expect(select_pickup_location_modal.pickup_locations_list).to_be_visible()

    select_pickup_location_modal.filter_countries_dropdown.select_item_by_name(country_to_filter)
    select_pickup_location_modal.filter_regions_dropdown.select_item_by_name(region_to_filter)
    select_pickup_location_modal.filter_cities_dropdown.select_item_by_name(city_to_filter)

    expect(select_pickup_location_modal.applied_filters_panel).to_be_visible()
    expect(select_pickup_location_modal.get_applied_filter_chip_by_name(country_to_filter).element).to_be_visible()
    expect(select_pickup_location_modal.get_applied_filter_chip_by_name(region_to_filter).element).to_be_visible()
    expect(select_pickup_location_modal.get_applied_filter_chip_by_name(city_to_filter).element).to_be_visible()
    expect(select_pickup_location_modal.reset_filters_chip).to_be_visible()

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )


@pytest.mark.e2e
@pytest.mark.checkout_mode("single-page")
def test_e2e_filter_pickup_locations_country_region_keyword_found_single_page_checkout(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to filter pickup locations by country, region with search keyword with positive results in single-page checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    product = dataset["products"][1]

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": 2,
        }
    )

    cart_page = CartPage(config, page)
    cart_page.navigate()

    country_to_filter = "United States of America"
    region_to_filter = "New York"
    keyword_to_search = "Empire"

    cart_page.shipping_details_section_component.pickup_delivery_option_switcher.click()
    cart_page.shipping_details_section_component.pickup_point_section.locator(
        "[data-test-id='select-address-button']"
    ).click()

    select_pickup_location_modal = SelectBopisMapModalComponent(page.locator(".select-address-map-modal"))

    select_pickup_location_modal.filter_countries_dropdown.select_item_by_name(country_to_filter)
    select_pickup_location_modal.filter_regions_dropdown.select_item_by_name(region_to_filter)
    select_pickup_location_modal.search_pickup_location_input.fill(keyword_to_search)
    select_pickup_location_modal.search_pickup_location_input.press("Enter")
    page.wait_for_load_state("networkidle")

    pickup_locations = select_pickup_location_modal.pickup_locations
    pickup_points = [
        pickup_point
        for pickup_point in pickup_locations
        if pickup_point.country == country_to_filter and pickup_point.region == "NY"
    ]

    assert len(pickup_points) >= 1, "No pickup locations found"
    assert select_pickup_location_modal.has_pickup_location_with_keyword(
        keyword_to_search
    ), f"No pickup location contains keyword '{keyword_to_search}'"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )


@pytest.mark.e2e
@pytest.mark.checkout_mode("single-page")
def test_e2e_filter_pickup_locations_country_region_city_keyword_found_single_page_checkout(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to filter pickup locations by country, region, city with search keyword with positive results in single-page checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    country_to_filter = "United States of America"
    region_to_filter = "New York"
    city_to_filter = "Manhattan"
    keyword_to_search = "5th"

    product = dataset["products"][1]

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": 2,
        }
    )

    cart_page = CartPage(config, page)
    cart_page.navigate()

    cart_page.shipping_details_section_component.pickup_delivery_option_switcher.click()
    cart_page.shipping_details_section_component.pickup_point_section.locator(
        "[data-test-id='select-address-button']"
    ).click()

    select_pickup_location_modal = SelectBopisMapModalComponent(page.locator(".select-address-map-modal"))

    select_pickup_location_modal.filter_countries_dropdown.select_item_by_name(country_to_filter)
    select_pickup_location_modal.filter_regions_dropdown.select_item_by_name(region_to_filter)
    select_pickup_location_modal.filter_cities_dropdown.select_item_by_name(city_to_filter)
    select_pickup_location_modal.search_pickup_location_input.fill(keyword_to_search)
    select_pickup_location_modal.search_pickup_location_input.press("Enter")
    page.wait_for_load_state("networkidle")

    pickup_locations = select_pickup_location_modal.pickup_locations
    pickup_points = [
        pickup_point
        for pickup_point in pickup_locations
        if pickup_point.country == country_to_filter
        and pickup_point.region == "NY"
        and pickup_point.city == city_to_filter
    ]

    assert len(pickup_points) >= 1, "No pickup locations found"
    assert select_pickup_location_modal.has_pickup_location_with_keyword(
        keyword_to_search
    ), f"No pickup location contains keyword '{keyword_to_search}'"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )


@pytest.mark.e2e
@pytest.mark.checkout_mode("single-page")
def test_e2e_filter_pickup_locations_country_region_city_keyword_not_found_single_page_checkout(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to filter pickup locations by country, region, city with search keyword with negative results in single-page checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    country_to_filter = "United States of America"
    region_to_filter = "New York"
    city_to_filter = "Manhattan"
    keyword_to_search = "NonExistent"

    product = dataset["products"][1]

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": 2,
        }
    )

    cart_page = CartPage(config, page)
    cart_page.navigate()

    cart_page.shipping_details_section_component.pickup_delivery_option_switcher.click()
    cart_page.shipping_details_section_component.pickup_point_section.locator(
        "[data-test-id='select-address-button']"
    ).click()

    select_pickup_location_modal = SelectBopisMapModalComponent(page.locator(".select-address-map-modal"))

    select_pickup_location_modal.filter_countries_dropdown.select_item_by_name(country_to_filter)
    select_pickup_location_modal.filter_regions_dropdown.select_item_by_name(region_to_filter)
    select_pickup_location_modal.filter_cities_dropdown.select_item_by_name(city_to_filter)
    select_pickup_location_modal.search_pickup_location_input.fill(keyword_to_search)
    select_pickup_location_modal.search_pickup_location_input.press("Enter")
    page.wait_for_load_state("networkidle")

    pickup_locations = select_pickup_location_modal.pickup_locations
    pickup_points = [
        pickup_point
        for pickup_point in pickup_locations
        if pickup_point.country == country_to_filter
        and pickup_point.region == region_to_filter
        and pickup_point.city == city_to_filter
    ]

    assert len(pickup_points) == 0, "Pickup locations found"
    assert not select_pickup_location_modal.has_pickup_location_with_keyword(
        keyword_to_search
    ), f"Pickup location contains keyword '{keyword_to_search}' when it shouldn't"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )


@pytest.mark.e2e
@pytest.mark.checkout_mode("single-page")
def test_e2e_filter_pickup_locations_remove_filters_single_page_checkout(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to remove filters from pickup point selection modal in single-page checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    country_to_filter = "United States of America"
    region_to_filter = "New York"
    city_to_filter = "Manhattan"
    keyword_to_search = "Fifth"

    product = dataset["products"][1]

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": 2,
        }
    )

    cart_page = CartPage(config, page)
    cart_page.navigate()

    cart_page.shipping_details_section_component.pickup_delivery_option_switcher.click()
    cart_page.shipping_details_section_component.pickup_point_section.locator(
        "[data-test-id='select-address-button']"
    ).click()

    select_pickup_location_modal = SelectBopisMapModalComponent(page.locator(".select-address-map-modal"))

    all_pickup_points_count = len(select_pickup_location_modal.pickup_locations)

    select_pickup_location_modal.filter_countries_dropdown.select_item_by_name(country_to_filter)
    select_pickup_location_modal.filter_regions_dropdown.select_item_by_name(region_to_filter)
    select_pickup_location_modal.filter_cities_dropdown.select_item_by_name(city_to_filter)
    select_pickup_location_modal.search_pickup_location_input.fill(keyword_to_search)
    select_pickup_location_modal.search_pickup_location_input.press("Enter")
    page.wait_for_load_state("networkidle")

    filtered_pickup_points_count = len(select_pickup_location_modal.pickup_locations)

    select_pickup_location_modal.get_applied_filter_chip_by_name(region_to_filter).close_chip()
    page.wait_for_load_state("networkidle")

    updated_pickup_points_count = len(select_pickup_location_modal.pickup_locations)

    select_pickup_location_modal.reset_filters_chip.click()
    page.wait_for_load_state("networkidle")
    # Wait for the pickup locations list to be fully re-populated after reset
    select_pickup_location_modal.pickup_locations_list.locator(
        f"[data-address-id^='pickup-location-']:nth-child({all_pickup_points_count})"
    ).wait_for(state="visible", timeout=10_000)

    restored_pickup_points_count = len(select_pickup_location_modal.pickup_locations)

    assert updated_pickup_points_count == filtered_pickup_points_count, "Pickup points count not updated"
    assert restored_pickup_points_count == all_pickup_points_count, "Pickup points count not restored"

    cart_operations.clear_cart(
        payload={
            "storeId": config["STORE_ID"],
            "cartId": cart["id"],
            "userId": user["id"],
            "currencyCode": dataset["currencies"][0]["code"],
            "cultureName": dataset["languages"][0]["allowedValues"][0],
        }
    )


@pytest.mark.e2e
@pytest.mark.checkout_mode("multi-step")
def test_e2e_filter_pickup_locations_elements_multi_step_checkout(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to check filter pickup locations elements on pickup point selection modal in multi-step checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    country_to_filter = "United States of America"
    region_to_filter = "New York"
    city_to_filter = "Manhattan"

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    product = dataset["products"][1]

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": 2,
        }
    )

    checkout_shipping_page = CheckoutShippingPage(config, page)
    checkout_shipping_page.navigate()
    page.wait_for_load_state("networkidle")

    checkout_shipping_page.shipping_details_section_component.pickup_delivery_option_switcher.click()
    checkout_shipping_page.shipping_details_section_component.pickup_point_section.locator(
        "[data-test-id='select-address-button']"
    ).click()

    select_pickup_location_modal = SelectBopisMapModalComponent(page.locator(".select-address-map-modal"))

    expect(select_pickup_location_modal.element).to_be_visible()
    expect(select_pickup_location_modal.pickup_locations_list).to_be_visible()

    select_pickup_location_modal.filter_countries_dropdown.select_item_by_name(country_to_filter)
    select_pickup_location_modal.filter_regions_dropdown.select_item_by_name(region_to_filter)
    select_pickup_location_modal.filter_cities_dropdown.select_item_by_name(city_to_filter)

    expect(select_pickup_location_modal.applied_filters_panel).to_be_visible()
    expect(select_pickup_location_modal.get_applied_filter_chip_by_name(country_to_filter).element).to_be_visible()
    expect(select_pickup_location_modal.get_applied_filter_chip_by_name(region_to_filter).element).to_be_visible()
    expect(select_pickup_location_modal.get_applied_filter_chip_by_name(city_to_filter).element).to_be_visible()
    expect(select_pickup_location_modal.reset_filters_chip).to_be_visible()

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
            "currencyCode": dataset["currencies"][0]["code"],
            "cultureName": dataset["languages"][0]["allowedValues"][0],
            "storeId": config["STORE_ID"],
        }
    )


@pytest.mark.e2e
@pytest.mark.checkout_mode("multi-step")
def test_e2e_filter_pickup_locations_country_region_keyword_found_multi_step_checkout(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to filter pickup locations by country, region with search keyword with positive results in multi-step checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": "product-acme-laptop-hp-pavilion-16-ag0087nr",
            "quantity": 2,
        }
    )

    checkout_shipping_page = CheckoutShippingPage(config, page)
    checkout_shipping_page.navigate()
    page.wait_for_load_state("networkidle")

    country_to_filter = "United States of America"
    region_to_filter = "New York"
    keyword_to_search = "Empire"

    checkout_shipping_page.shipping_details_section_component.pickup_delivery_option_switcher.click()
    checkout_shipping_page.shipping_details_section_component.pickup_point_section.locator(
        "[data-test-id='select-address-button']"
    ).click()

    select_pickup_location_modal = SelectBopisMapModalComponent(page.locator(".select-address-map-modal"))

    select_pickup_location_modal.filter_countries_dropdown.select_item_by_name(country_to_filter)
    select_pickup_location_modal.filter_regions_dropdown.select_item_by_name(region_to_filter)
    select_pickup_location_modal.search_pickup_location_input.fill(keyword_to_search)
    select_pickup_location_modal.search_pickup_location_input.press("Enter")
    page.wait_for_load_state("networkidle")

    pickup_locations = select_pickup_location_modal.pickup_locations
    pickup_points = [
        pickup_point
        for pickup_point in pickup_locations
        if pickup_point.country == country_to_filter and pickup_point.region == "NY"
    ]

    assert len(pickup_points) >= 1, "No pickup locations found"
    assert select_pickup_location_modal.has_pickup_location_with_keyword(
        keyword_to_search
    ), f"No pickup location contains keyword '{keyword_to_search}'"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
            "currencyCode": dataset["currencies"][0]["code"],
            "cultureName": dataset["languages"][0]["allowedValues"][0],
            "storeId": config["STORE_ID"],
        }
    )


@pytest.mark.e2e
@pytest.mark.checkout_mode("multi-step")
def test_e2e_filter_pickup_locations_country_region_city_keyword_found_multi_step_checkout(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to filter pickup locations by country, region, city with search keyword with positive results in multi-step checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    country_to_filter = "United States of America"
    region_to_filter = "New York"
    city_to_filter = "Manhattan"
    keyword_to_search = "5th"

    product = dataset["products"][1]

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": 2,
        }
    )

    checkout_shipping_page = CheckoutShippingPage(config, page)
    checkout_shipping_page.navigate()
    page.wait_for_load_state("networkidle")

    checkout_shipping_page.shipping_details_section_component.pickup_delivery_option_switcher.click()
    checkout_shipping_page.shipping_details_section_component.pickup_point_section.locator(
        "[data-test-id='select-address-button']"
    ).click()

    select_pickup_location_modal = SelectBopisMapModalComponent(page.locator(".select-address-map-modal"))

    select_pickup_location_modal.filter_countries_dropdown.select_item_by_name(country_to_filter)
    select_pickup_location_modal.filter_regions_dropdown.select_item_by_name(region_to_filter)
    select_pickup_location_modal.filter_cities_dropdown.select_item_by_name(city_to_filter)
    select_pickup_location_modal.search_pickup_location_input.fill(keyword_to_search)
    select_pickup_location_modal.search_pickup_location_input.press("Enter")
    page.wait_for_load_state("networkidle")

    pickup_locations = select_pickup_location_modal.pickup_locations
    pickup_points = [
        pickup_point
        for pickup_point in pickup_locations
        if pickup_point.country == country_to_filter
        and pickup_point.region == "NY"
        and pickup_point.city == city_to_filter
    ]

    assert len(pickup_points) >= 1, "No pickup locations found"
    assert select_pickup_location_modal.has_pickup_location_with_keyword(
        keyword_to_search
    ), f"No pickup location contains keyword '{keyword_to_search}'"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
            "currencyCode": dataset["currencies"][0]["code"],
            "cultureName": dataset["languages"][0]["allowedValues"][0],
            "storeId": config["STORE_ID"],
        }
    )


@pytest.mark.e2e
@pytest.mark.checkout_mode("multi-step")
def test_e2e_filter_pickup_locations_country_region_city_keyword_not_found_multi_step_checkout(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to filter pickup locations by country, region, city with search keyword with negative results in multi-step checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    country_to_filter = "United States of America"
    region_to_filter = "New York"
    city_to_filter = "Manhattan"
    keyword_to_search = "NonExistent"

    product = dataset["products"][1]

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": 2,
        }
    )

    checkout_shipping_page = CheckoutShippingPage(config, page)
    checkout_shipping_page.navigate()
    page.wait_for_load_state("networkidle")

    checkout_shipping_page.shipping_details_section_component.pickup_delivery_option_switcher.click()
    checkout_shipping_page.shipping_details_section_component.pickup_point_section.locator(
        "[data-test-id='select-address-button']"
    ).click()

    select_pickup_location_modal = SelectBopisMapModalComponent(page.locator(".select-address-map-modal"))

    select_pickup_location_modal.filter_countries_dropdown.select_item_by_name(country_to_filter)
    select_pickup_location_modal.filter_regions_dropdown.select_item_by_name(region_to_filter)
    select_pickup_location_modal.filter_cities_dropdown.select_item_by_name(city_to_filter)
    select_pickup_location_modal.search_pickup_location_input.fill(keyword_to_search)
    select_pickup_location_modal.search_pickup_location_input.press("Enter")
    page.wait_for_load_state("networkidle")

    pickup_locations = select_pickup_location_modal.pickup_locations
    pickup_points = [
        pickup_point
        for pickup_point in pickup_locations
        if pickup_point.country == country_to_filter
        and pickup_point.region == region_to_filter
        and pickup_point.city == city_to_filter
    ]

    assert len(pickup_points) == 0, "Pickup locations found"
    assert not select_pickup_location_modal.has_pickup_location_with_keyword(
        keyword_to_search
    ), f"Pickup location contains keyword '{keyword_to_search}' when it shouldn't"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
            "currencyCode": dataset["currencies"][0]["code"],
            "cultureName": dataset["languages"][0]["allowedValues"][0],
            "storeId": config["STORE_ID"],
        }
    )


@pytest.mark.e2e
@pytest.mark.checkout_mode("multi-step")
def test_e2e_filter_pickup_locations_remove_filters_multi_step_checkout(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to remove filters from pickup point selection modal in multi-step checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    country_to_filter = "United States of America"
    region_to_filter = "New York"
    city_to_filter = "Manhattan"
    keyword_to_search = "Fifth"

    product = dataset["products"][1]

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": 2,
        }
    )

    checkout_shipping_page = CheckoutShippingPage(config, page)
    checkout_shipping_page.navigate()
    page.wait_for_load_state("networkidle")

    checkout_shipping_page.shipping_details_section_component.pickup_delivery_option_switcher.click()
    checkout_shipping_page.shipping_details_section_component.pickup_point_section.locator(
        "[data-test-id='select-address-button']"
    ).click()

    select_pickup_location_modal = SelectBopisMapModalComponent(page.locator(".select-address-map-modal"))

    all_pickup_points_count = len(select_pickup_location_modal.pickup_locations)

    select_pickup_location_modal.filter_countries_dropdown.select_item_by_name(country_to_filter)
    select_pickup_location_modal.filter_regions_dropdown.select_item_by_name(region_to_filter)
    select_pickup_location_modal.filter_cities_dropdown.select_item_by_name(city_to_filter)
    select_pickup_location_modal.search_pickup_location_input.fill(keyword_to_search)
    select_pickup_location_modal.search_pickup_location_input.press("Enter")
    page.wait_for_load_state("networkidle")

    filtered_pickup_points_count = len(select_pickup_location_modal.pickup_locations)

    select_pickup_location_modal.get_applied_filter_chip_by_name(region_to_filter).close_chip()

    updated_pickup_points_count = len(select_pickup_location_modal.pickup_locations)

    select_pickup_location_modal.reset_filters_chip.click()
    page.wait_for_load_state("networkidle")
    select_pickup_location_modal.pickup_locations_list.locator(
        f"[data-address-id^='pickup-location-']:nth-child({all_pickup_points_count})"
    ).wait_for(state="visible", timeout=10_000)

    restored_pickup_points_count = len(select_pickup_location_modal.pickup_locations)

    assert updated_pickup_points_count == filtered_pickup_points_count, "Pickup points count not updated"
    assert restored_pickup_points_count == all_pickup_points_count, "Pickup points count not restored"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
            "currencyCode": dataset["currencies"][0]["code"],
            "cultureName": dataset["languages"][0]["allowedValues"][0],
            "storeId": config["STORE_ID"],
        }
    )
