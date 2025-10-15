import os
import time
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.requests_tracker import RequestsTracker
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage
from tests_e2e.pages.checkout_billing_page import CheckoutBillingPage
from tests_e2e.pages.checkout_completed_page import CheckoutCompletedPage
from tests_e2e.pages.checkout_review_order_page import CheckoutReviewOrderPage
from tests_e2e.pages.checkout_shipping_page import CheckoutShippingPage
from tests_e2e.pages.sign_in_page import SignInPage


@pytest.mark.e2e
@allure.title("Create order - multi-step checkout (E2E)")
def test_e2e_create_order_multi_step_checkout(
    config: dict[str, Any],
    dataset: dict[str, Any],
    page: Page,
    requests_tracker: RequestsTracker,
    product_quantity_control: str,
    checkout_mode: str,
):
    if checkout_mode == "single-page":
        pytest.skip("Checkout mode is a multi-step")

    print(
        f"{os.linesep}Running E2E test to create order in multi-step checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(dataset["users"][0]["userName"], config["users_password"])

    expect(page).not_to_have_url(sign_in_page.url), "Sign in page is still visible"

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

    expect(page).to_have_url(
        checkout_shipping_page.url
    ), "Checkout shipping page is not loaded"

    checkout_shipping_page.shipping_details_section_component.switch_delivery_option(
        "shipping"
    )

    expect(
        checkout_shipping_page.shipping_details_section_component.address_selector_component.element
    ).to_be_visible(), "Shipping address section is not visible"
    expect(
        checkout_shipping_page.shipping_details_section_component.shipping_method_selector
    ).to_be_visible(), "Shipping method selector is not visible"
    expect(
        checkout_shipping_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).to_be_visible(), "Selected address label is not visible"
    expect(
        checkout_shipping_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).not_to_be_empty(), "Selected address label is empty"

    checkout_shipping_page.shipping_details_section_component.select_shipping_method(
        "FixedRate_Ground"
    )

    requests_tracker.wait_for_all_requests()

    expect(
        checkout_shipping_page.billing_button
    ).to_be_visible(), "Billing button is not visible"
    expect(
        checkout_shipping_page.billing_button
    ).to_be_enabled(), "Billing button is disabled"

    checkout_shipping_page.billing_button.click()

    checkout_billing_page = CheckoutBillingPage(config, page)

    expect(page).to_have_url(
        checkout_billing_page.url
    ), "Checkout billing page is not loaded"
    expect(
        checkout_billing_page.payment_details_section_component.element
    ).to_be_visible(), "Payment details section is not visible"

    checkout_billing_page.payment_details_section_component.select_payment_method(
        "DefaultManualPaymentMethod"
    )

    requests_tracker.wait_for_all_requests()

    expect(
        checkout_billing_page.review_order_button
    ).to_be_visible(), "Review order button is not visible"
    expect(
        checkout_billing_page.review_order_button
    ).to_be_enabled(), "Review order button is disabled"

    checkout_billing_page.review_order_button.click()

    checkout_review_order_page = CheckoutReviewOrderPage(config, page)

    expect(page).to_have_url(
        checkout_review_order_page.url
    ), "Checkout review order page is not loaded"
    expect(
        checkout_review_order_page.place_order_button
    ).to_be_visible(), "Place order button is not visible"
    expect(
        checkout_review_order_page.place_order_button
    ).to_be_enabled(), "Place order button is disabled"

    checkout_review_order_page.place_order_button.click()

    checkout_completed_page = CheckoutCompletedPage(config, page)

    expect(page).to_have_url(
        checkout_completed_page.url
    ), "Checkout completed page is not loaded"

    print(f"Order number: {checkout_completed_page.order_number}")
    assert checkout_completed_page.order_number is not None, "Order number is not found"


@pytest.mark.e2e
@allure.title("Create order - single-page checkout (E2E)")
def test_e2e_create_order_single_page_checkout(
    config: dict[str, Any],
    dataset: dict[str, Any],
    page: Page,
    requests_tracker: RequestsTracker,
    product_quantity_control: str,
    checkout_mode: str,
):
    if checkout_mode == "multi-step":
        pytest.skip("Checkout mode is a single-page")

    print(
        f"{os.linesep}Running E2E test to create order in multi-step checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(dataset["users"][0]["userName"], config["users_password"])

    expect(page).not_to_have_url(sign_in_page.url), "Sign in page is still visible"

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

    expect(page).to_have_url(cart_page.url), "Cart page is not loaded"
    expect(
        cart_page.shipping_details_section_component.element
    ).to_be_visible(), "Shipping details section is not visible"

    cart_page.shipping_details_section_component.shipping_delivery_option_switcher.click()

    expect(
        cart_page.shipping_details_section_component.address_selector_component.element
    ).to_be_visible(), "Shipping address section is not visible"
    expect(
        cart_page.shipping_details_section_component.shipping_method_selector
    ).to_be_visible(), "Shipping method selector is not visible"
    expect(
        cart_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).to_be_visible(), "Selected address label is not visible"
    expect(
        cart_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).not_to_be_empty(), "Selected address label is empty"

    cart_page.shipping_details_section_component.select_shipping_method(
        "FixedRate_Ground"
    )

    requests_tracker.wait_for_all_requests()

    expect(
        cart_page.payment_details_section_component.element
    ).to_be_visible(), "Payment details section is not visible"

    cart_page.payment_details_section_component.select_payment_method(
        "DefaultManualPaymentMethod"
    )

    requests_tracker.wait_for_all_requests()

    expect(
        cart_page.place_order_button
    ).to_be_visible(), "Place order button is not visible"
    expect(
        cart_page.place_order_button
    ).to_be_enabled(), "Place order button is disabled"

    cart_page.place_order_button.click()

    checkout_completed_page = CheckoutCompletedPage(config, page)

    expect(page).to_have_url(
        checkout_completed_page.url
    ), "Checkout completed page is not loaded"

    print(f"Order number: {checkout_completed_page.order_number}")
    assert checkout_completed_page.order_number is not None, "Order number is not found"
