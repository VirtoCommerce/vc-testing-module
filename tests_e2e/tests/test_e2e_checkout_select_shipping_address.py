import os
import time
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from tests_e2e.components.select_address_modal_component import (
    SelectAddressModalComponent,
)
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage
from tests_e2e.pages.checkout_shipping_page import CheckoutShippingPage
from tests_e2e.pages.sign_in_page import SignInPage


@pytest.mark.e2e
@allure.title("Select shipping address in single-page checkout (E2E)")
def test_e2e_single_page_checkout_select_shipping_address(
    config: dict[str, Any],
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
        f"{os.linesep}Running E2E test to select a shipping address in single-page checkout...",
        end=" ",
    )

    anonymous_catalog_requests.toggle(True)
    page.set_viewport_size({"width": 1920, "height": 1080})

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(dataset["users"][0]["userName"], config["users_password"])
    time.sleep(2)

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
        cart_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).to_be_visible()
    expect(
        cart_page.shipping_details_section_component.address_selector_component.select_address_button
    ).to_be_visible()

    cart_page.shipping_details_section_component.address_selector_component.select_address_button.click()

    select_address_modal = SelectAddressModalComponent(
        page.locator("[data-test-id='select-address-modal']")
    )

    expect(select_address_modal.element).to_be_visible()
    expect(select_address_modal.items[0]).to_be_visible()

    select_address_modal.items[0].click()

    expect(select_address_modal.confirm_button).to_be_visible()
    expect(select_address_modal.confirm_button).to_be_enabled()

    select_address_modal.confirm_button.click()

    expect(
        cart_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).to_be_visible()
    expect(
        cart_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).not_to_be_empty()

    cart_page.clear_cart()
    cart_page.sign_out()


@pytest.mark.e2e
@allure.title("Select shipping address in multi-step checkout (E2E)")
def test_e2e_multi_step_checkout_select_shipping_address(
    config: dict[str, Any],
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
        f"{os.linesep}Running E2E test to select a shipping address in multi-step checkout...",
        end=" ",
    )

    anonymous_catalog_requests.toggle(True)
    page.set_viewport_size({"width": 1920, "height": 1080})

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(dataset["users"][0]["userName"], config["users_password"])
    time.sleep(2)

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
        checkout_shipping_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).to_be_visible()
    expect(
        checkout_shipping_page.shipping_details_section_component.address_selector_component.select_address_button
    ).to_be_visible()

    checkout_shipping_page.shipping_details_section_component.address_selector_component.select_address_button.click()

    select_address_modal = SelectAddressModalComponent(
        page.locator("[data-test-id='select-address-modal']")
    )

    expect(select_address_modal.element).to_be_visible()
    expect(select_address_modal.items[0]).to_be_visible()

    select_address_modal.items[0].click()

    expect(select_address_modal.confirm_button).to_be_visible()
    expect(select_address_modal.confirm_button).to_be_enabled()

    select_address_modal.confirm_button.click()

    expect(
        checkout_shipping_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).to_be_visible()
    expect(
        checkout_shipping_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).not_to_be_empty()

    cart_page.navigate()
    cart_page.clear_cart()
    cart_page.sign_out()
