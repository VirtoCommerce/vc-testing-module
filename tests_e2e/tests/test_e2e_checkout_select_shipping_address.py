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
from tests_e2e.pages import CartPage, CheckoutShippingPage


@pytest.mark.e2e
def test_e2e_single_page_checkout_select_shipping_address(
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
        f"{os.linesep}Running E2E test to select a shipping address in single-page checkout...",
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

    cart_page = CartPage(config, page)
    cart_page.navigate()

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

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )


@pytest.mark.e2e
def test_e2e_multi_step_checkout_select_shipping_address(
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
        f"{os.linesep}Running E2E test to select a shipping address in multi-step checkout...",
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

    auth.set_local_storage_user_id(page, user["id"])

    checkout_shipping_page = CheckoutShippingPage(config, page)
    checkout_shipping_page.navigate()

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

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )
