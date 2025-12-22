import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from fixtures.config import Config
from tests_e2e.components.edit_address_modal_component import EditAddressModalComponent
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage
from tests_e2e.pages.checkout_shipping_page import CheckoutShippingPage


@pytest.mark.e2e
@allure.title("Add shipping address in anonymous single-page checkout (E2E)")
def test_e2e_anonymous_single_page_checkout_add_shipping_address(
    config: Config,
    dataset: dict[str, Any],
    anonymous_catalog_requests: AnonymousCatalogRequests,
    product_quantity_control: str,
    checkout_mode: str,
    page: Page,
):
    if checkout_mode == "multi-step":
        pytest.skip(
            "Checkout mode is a multi-step, skipping test for single-page checkout"
        )

    print(
        f"{os.linesep}Running E2E test to add a shipping address in anonymous single-page checkout...",
        end=" ",
    )

    anonymous_catalog_requests.toggle(True)
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

    expect(
        cart_page.shipping_details_section_component.address_selector_component.select_address_button
    ).to_be_visible()

    cart_page.shipping_details_section_component.address_selector_component.select_address_button.click()

    edit_address_modal = EditAddressModalComponent(
        page.locator("[data-test-id='edit-address-modal']")
    )

    expect(edit_address_modal.element).to_be_visible()

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

    edit_address_modal.address_form_component.fill_address(test_address)

    expect(edit_address_modal.submit_button).to_be_enabled()

    edit_address_modal.submit_button.click()

    expect(
        cart_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).to_be_visible()

    cart_page.clear_cart()


@pytest.mark.e2e
@allure.title("Add shipping address in anonymous multi-step checkout (E2E)")
def test_e2e_anonymous_multi_step_checkout_add_shipping_address(
    config: Config,
    dataset: dict[str, Any],
    anonymous_catalog_requests: AnonymousCatalogRequests,
    product_quantity_control: str,
    checkout_mode: str,
    page: Page,
):
    if checkout_mode == "single-page":
        pytest.skip(
            "Checkout mode is a single-page, skipping test for multi-step checkout"
        )

    print(
        f"{os.linesep}Running E2E test to add a shipping address in anonymous multi-step checkout...",
        end=" ",
    )

    anonymous_catalog_requests.toggle(True)
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

    expect(
        checkout_shipping_page.shipping_details_section_component.address_selector_component.select_address_button
    ).to_be_visible()

    checkout_shipping_page.shipping_details_section_component.address_selector_component.select_address_button.click()

    edit_address_modal = EditAddressModalComponent(
        page.locator("[data-test-id='edit-address-modal']")
    )

    expect(edit_address_modal.element).to_be_visible()

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

    edit_address_modal.address_form_component.fill_address(test_address)

    expect(edit_address_modal.submit_button).to_be_enabled()

    edit_address_modal.submit_button.click()

    expect(
        checkout_shipping_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).to_be_visible()

    cart_page.navigate()
    cart_page.clear_cart()
