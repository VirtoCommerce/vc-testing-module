from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures.config import Config
from tests_e2e.components.select_bopis_map_modal_component import (
    SelectBopisMapModalComponent,
)
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage
from tests_e2e.pages.checkout_shipping_page import CheckoutShippingPage


@pytest.mark.e2e
def test_e2e_select_pickup_location_single_page_checkout(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    product_quantity_control: str,
    checkout_mode: str,
):
    if checkout_mode == "multi-step":
        pytest.skip(
            "Checkout mode is a single-page, skipping test for multi-step checkout"
        )

    page.set_viewport_size({"width": 1920, "height": 1080})

    category_to_browse = next(
        category
        for category in dataset["categories"]
        if category["id"] == "category-acme-laptops"
    )
    product_to_add_to_cart = next(
        product
        for product in dataset["products"]
        if product["id"] == "product-acme-laptop-hp-pavilion-16-ag0087nr"
    )

    category_page = CategoryPage(
        config,
        page,
        category_to_browse["seoInfos"][0]["semanticUrl"],
        product_quantity_control,
    )
    category_page.navigate()
    category_page.add_product_to_cart(product_to_add_to_cart["code"], 2)

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


@pytest.mark.e2e
def test_e2e_select_pickup_location_multi_step_checkout(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    product_quantity_control: str,
    checkout_mode: str,
):
    if checkout_mode == "single-page":
        pytest.skip(
            "Checkout mode is a multi-step, skipping test for single-page checkout"
        )

    page.set_viewport_size({"width": 1920, "height": 1080})

    category_to_browse = next(
        category
        for category in dataset["categories"]
        if category["id"] == "category-acme-laptops"
    )
    product_to_add_to_cart = next(
        product
        for product in dataset["products"]
        if product["id"] == "product-acme-laptop-hp-pavilion-16-ag0087nr"
    )

    category_page = CategoryPage(
        config,
        page,
        category_to_browse["seoInfos"][0]["semanticUrl"],
        product_quantity_control,
    )
    category_page.navigate()
    category_page.add_product_to_cart(product_to_add_to_cart["code"], 2)

    cart_page = CartPage(config, page)
    cart_page.navigate()
    cart_page.checkout_button.click()

    checkout_shipping_page = CheckoutShippingPage(config, page)

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
