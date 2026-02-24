import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.components.edit_address_modal_component import EditAddressModalComponent
from tests_e2e.pages import CartPage, CheckoutShippingPage


@pytest.mark.e2e
@pytest.mark.checkout_mode("single-page")
def test_e2e_anonymous_single_page_checkout_add_shipping_address(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    dataset: dict[str, Any],
    page: Page,
):

    print(
        f"{os.linesep}Running E2E test to add a shipping address in anonymous single-page checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

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

    auth.set_local_storage_user_id(page, user["id"])

    cart_page = CartPage(config, page)
    cart_page.navigate()

    expect(
        cart_page.shipping_details_section_component.address_selector_component.select_address_button
    ).to_be_visible()

    cart_page.shipping_details_section_component.address_selector_component.select_address_button.click()

    edit_address_modal = EditAddressModalComponent(page.locator("[data-test-id='edit-address-modal']"))

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

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )


@pytest.mark.e2e
@pytest.mark.checkout_mode("multi-step")
def test_e2e_anonymous_multi_step_checkout_add_shipping_address(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
):

    print(
        f"{os.linesep}Running E2E test to add a shipping address in anonymous multi-step checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_me()
    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "productId": "product-acme-laptop-hp-pavilion-16-ag0087nr",
            "quantity": 2,
        }
    )

    auth.set_local_storage_user_id(page, user["id"])

    checkout_shipping_page = CheckoutShippingPage(config, page)
    checkout_shipping_page.navigate()

    expect(
        checkout_shipping_page.shipping_details_section_component.address_selector_component.select_address_button
    ).to_be_visible()

    checkout_shipping_page.shipping_details_section_component.address_selector_component.select_address_button.click()

    edit_address_modal = EditAddressModalComponent(page.locator("[data-test-id='edit-address-modal']"))

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

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )
