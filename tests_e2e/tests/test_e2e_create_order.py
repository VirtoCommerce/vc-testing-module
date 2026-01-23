import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.components.select_address_modal_component import (
    SelectAddressModalComponent,
)
from tests_e2e.pages import (
    CartPage,
    CheckoutBillingPage,
    CheckoutCompletedPage,
    CheckoutReviewOrderPage,
    CheckoutShippingPage,
)


@pytest.mark.e2e
def test_e2e_create_order_multi_step_checkout(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
):
    if config["CHECKOUT_MODE"] == "single-page":
        pytest.skip(
            "Checkout mode is a single-page, skipping test for multi-step checkout"
        )

    print(
        f"{os.linesep}Running E2E test to create order in multi-step checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    product = dataset["products"][1]

    user = user_operations.get_me()
    cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": 2,
        }
    )

    checkout_shipping_page = CheckoutShippingPage(config, page)
    checkout_shipping_page.navigate()

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
def test_e2e_create_order_single_page_checkout(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
):
    if config["CHECKOUT_MODE"] == "multi-step":
        pytest.skip(
            "Checkout mode is a multi-step, skipping test for single-page checkout"
        )

    print(
        f"{os.linesep}Running E2E test to create order in multi-step checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

    product = dataset["products"][1]

    user = user_operations.get_me()
    cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": product["code"],
            "quantity": 2,
        }
    )

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

    if (
        not cart_page.shipping_details_section_component.address_selector_component.selected_address_label.is_visible()
    ):
        cart_page.shipping_details_section_component.address_selector_component.select_address_button.click()
        select_address_modal = SelectAddressModalComponent(
            page.locator("[data-test-id='select-address-modal']")
        )
        select_address_modal.items[0].click()
        select_address_modal.confirm_button.click()

    expect(
        cart_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).to_be_visible(), "Selected address label is not visible"
    expect(
        cart_page.shipping_details_section_component.address_selector_component.selected_address_label
    ).not_to_be_empty(), "Selected address label is empty"

    cart_page.shipping_details_section_component.select_shipping_method(
        "FixedRate_Ground"
    )

    expect(
        cart_page.payment_details_section_component.element
    ).to_be_visible(), "Payment details section is not visible"

    cart_page.payment_details_section_component.select_payment_method(
        "DefaultManualPaymentMethod"
    )

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

    assert checkout_completed_page.order_number is not None, "Order number is not found"
