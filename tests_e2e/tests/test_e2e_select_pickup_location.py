from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.components.select_bopis_map_modal_component import (
    SelectBopisMapModalComponent,
)
from tests_e2e.pages import CartPage, CheckoutShippingPage


@pytest.mark.ignore
@pytest.mark.e2e
@allure.title("Select pickup location in single-page checkout (E2E)")
def test_e2e_select_pickup_location_single_page_checkout(
    config: Config,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
    page: Page,
    auth: Auth,
):
    if config["CHECKOUT_MODE"] == "multi-step":
        pytest.skip(
            "Checkout mode is a single-page, skipping test for multi-step checkout"
        )

    page.set_viewport_size({"width": 1920, "height": 1080})

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

    select_pickup_location_modal = SelectBopisMapModalComponent(
        page.locator(".select-address-map-modal")
    )
    page.wait_for_selector("gmp-advanced-marker")

    expect(
        select_pickup_location_modal.element
    ).to_be_visible(), "Select address modal is not visible"
    expect(
        select_pickup_location_modal.pickup_locations_list
    ).to_be_visible(), "Pickup locations list is not visible"
    expect(
        select_pickup_location_modal.map_element
    ).to_be_visible(), "Map element is not visible"

    pickup_location_to_select = select_pickup_location_modal.get_location_by_name(
        "Atlantic Terminal Mall"
    )
    pickup_location_map_marker = (
        select_pickup_location_modal.get_map_marker_by_location_name(
            "Atlantic Terminal Mall"
        )
    )

    expect(
        pickup_location_to_select.element
    ).to_be_visible(), "Pickup location is not visible"
    expect(
        pickup_location_map_marker
    ).to_be_visible(), "Pickup location map marker is not visible"

    pickup_location_to_select.element.click()

    expect(select_pickup_location_modal.save_button).to_be_enabled()

    assert pickup_location_to_select.is_selected, "Pickup location is not selected"
    assert (
        pickup_location_map_marker.locator("gmp-pin").get_attribute("background")
        == "var(--color-success-500)"
    )

    select_pickup_location_modal.save_button.click()

    expect(
        select_pickup_location_modal.element
    ).not_to_be_visible(), "Select address modal is not closed"
    expect(
        cart_page.shipping_details_section_component.pickup_point_section.locator(
            "[data-test-id='selected-address-label']"
        )
    ).to_be_visible(), "Selected address label is not visible"


@pytest.mark.ignore
@pytest.mark.e2e
@allure.title("Select pickup location in multi-step checkout (E2E)")
def test_e2e_select_pickup_location_multi_step_checkout(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    auth: Auth,
    graphql_client: GraphQLClient,
):
    if config["CHECKOUT_MODE"] == "single-page":
        pytest.skip(
            "Checkout mode is a multi-step, skipping test for single-page checkout"
        )

    page.set_viewport_size({"width": 1920, "height": 1080})

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

    checkout_shipping_page.shipping_details_section_component.pickup_delivery_option_switcher.click()
    checkout_shipping_page.shipping_details_section_component.pickup_point_section.locator(
        "[data-test-id='select-address-button']"
    ).click()

    select_pickup_location_modal = SelectBopisMapModalComponent(
        page.locator(".select-address-map-modal")
    )
    page.wait_for_selector("gmp-advanced-marker")

    expect(
        select_pickup_location_modal.element
    ).to_be_visible(), "Select address modal is not visible"
    expect(
        select_pickup_location_modal.pickup_locations_list
    ).to_be_visible(), "Pickup locations list is not visible"
    expect(
        select_pickup_location_modal.map_element
    ).to_be_visible(), "Map element is not visible"

    pickup_location_to_select = select_pickup_location_modal.get_location_by_name(
        "Atlantic Terminal Mall"
    )
    pickup_location_map_marker = (
        select_pickup_location_modal.get_map_marker_by_location_name(
            "Atlantic Terminal Mall"
        )
    )

    expect(
        pickup_location_to_select.element
    ).to_be_visible(), "Pickup location is not visible"
    expect(
        pickup_location_map_marker
    ).to_be_visible(), "Pickup location map marker is not visible"

    pickup_location_to_select.element.click()

    expect(select_pickup_location_modal.save_button).to_be_enabled()

    assert pickup_location_to_select.is_selected, "Pickup location is not selected"
    assert (
        pickup_location_map_marker.locator("gmp-pin").get_attribute("background")
        == "var(--color-success-500)"
    )

    select_pickup_location_modal.save_button.click()

    expect(
        select_pickup_location_modal.element
    ).not_to_be_visible(), "Select address modal is not closed"
    expect(
        checkout_shipping_page.shipping_details_section_component.pickup_point_section.locator(
            "[data-test-id='selected-address-label']"
        )
    ).to_be_visible(), "Selected address label is not visible"
