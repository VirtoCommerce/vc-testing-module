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

    product = dataset["products"][14]

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

    expect(page, "Checkout shipping page is not loaded").to_have_url(
        checkout_shipping_page.url
    )

    checkout_shipping_page.shipping_details_section_component.switch_delivery_option(
        "shipping"
    )

    expect(
        checkout_shipping_page.shipping_details_section_component.address_selector_component.element,
        "Shipping address section is not visible",
    ).to_be_visible()
    expect(
        checkout_shipping_page.shipping_details_section_component.shipping_method_selector,
        "Shipping method selector is not visible",
    ).to_be_visible()
    expect(
        checkout_shipping_page.shipping_details_section_component.address_selector_component.selected_address_label,
        "Selected address label is not visible",
    ).to_be_visible()
    expect(
        checkout_shipping_page.shipping_details_section_component.address_selector_component.selected_address_label,
        "Selected address label is empty",
    ).not_to_be_empty()

    checkout_shipping_page.shipping_details_section_component.select_shipping_method(
        "FixedRate_Ground"
    )

    expect(
        checkout_shipping_page.billing_button,
        "Billing button is not visible",
    ).to_be_visible()
    expect(
        checkout_shipping_page.billing_button,
        "Billing button is disabled",
    ).to_be_enabled()

    checkout_shipping_page.billing_button.click()

    checkout_billing_page = CheckoutBillingPage(config, page)

    expect(page, "Checkout billing page is not loaded").to_have_url(
        checkout_billing_page.url
    )
    expect(
        checkout_billing_page.payment_details_section_component.element,
        "Payment details section is not visible",
    ).to_be_visible()

    checkout_billing_page.payment_details_section_component.select_payment_method(
        "DefaultManualPaymentMethod"
    )

    expect(
        checkout_billing_page.review_order_button,
        "Review order button is not visible",
    ).to_be_visible()
    expect(
        checkout_billing_page.review_order_button,
        "Review order button is disabled",
    ).to_be_enabled()

    checkout_billing_page.review_order_button.click()

    checkout_review_order_page = CheckoutReviewOrderPage(config, page)

    expect(page, "Checkout review order page is not loaded").to_have_url(
        checkout_review_order_page.url
    )
    expect(
        checkout_review_order_page.place_order_button,
        "Place order button is not visible",
    ).to_be_visible()
    expect(
        checkout_review_order_page.place_order_button,
        "Place order button is disabled",
    ).to_be_enabled()

    checkout_review_order_page.place_order_button.click()
    page.wait_for_load_state("networkidle")

    checkout_completed_page = CheckoutCompletedPage(config, page)

    expect(page, "Checkout completed page is not loaded").to_have_url(
        checkout_completed_page.url
    )

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

    product = dataset["products"][14]

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

    expect(page, "Cart page is not loaded").to_have_url(cart_page.url)
    assert (
        cart_page.shipping_details_section_component is not None
    ), "Shipping details section component is not found"
    expect(
        cart_page.shipping_details_section_component.element,
        "Shipping details section is not visible",
    ).to_be_visible()

    cart_page.shipping_details_section_component.shipping_delivery_option_switcher.click()

    expect(
        cart_page.shipping_details_section_component.address_selector_component.element,
        "Shipping address section is not visible",
    ).to_be_visible()
    expect(
        cart_page.shipping_details_section_component.shipping_method_selector,
        "Shipping method selector is not visible",
    ).to_be_visible()

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
        cart_page.shipping_details_section_component.address_selector_component.selected_address_label,
        "Selected address label is not visible",
    ).to_be_visible()
    expect(
        cart_page.shipping_details_section_component.address_selector_component.selected_address_label,
        "Selected address label is empty",
    ).not_to_be_empty()

    cart_page.shipping_details_section_component.select_shipping_method(
        "FixedRate_Ground"
    )

    assert (
        cart_page.payment_details_section_component is not None
    ), "Payment details section component is not found"
    expect(
        cart_page.payment_details_section_component.element,
        "Payment details section is not visible",
    ).to_be_visible()

    cart_page.payment_details_section_component.select_payment_method(
        "DefaultManualPaymentMethod"
    )

    expect(
        cart_page.place_order_button,
        "Place order button is not visible",
    ).to_be_visible()
    expect(
        cart_page.place_order_button,
        "Place order button is disabled",
    ).to_be_enabled()

    cart_page.place_order_button.click()
    page.wait_for_load_state("networkidle")

    checkout_completed_page = CheckoutCompletedPage(config, page)

    expect(page, "Checkout completed page is not loaded").to_have_url(
        checkout_completed_page.url
    )

    assert checkout_completed_page.order_number is not None, "Order number is not found"
