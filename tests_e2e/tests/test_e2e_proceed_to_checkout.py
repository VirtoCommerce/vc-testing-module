import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import CartPage, CategoryPage, CheckoutShippingPage, SignInPage


@pytest.mark.e2e
def test_e2e_proceed_to_multi_step_checkout(
    config: Config,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
    page: Page,
    auth: Auth,
):
    if config["CHECKOUT_MODE"] == "single-page":
        pytest.skip("Checkout mode is a multi-step")

    print(f"{os.linesep}Running E2E test to proceed to multi-step checkout...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    product = dataset["products"][1]

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

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

    expect(cart_page.checkout_button).to_be_visible(), "Checkout button is not visible"
    expect(cart_page.checkout_button).to_be_enabled(), "Checkout button is not enabled"

    cart_page.checkout_button.click()

    checkout_page = CheckoutShippingPage(config, page)

    expect(checkout_page.page).to_have_url(
        checkout_page.url
    ), "Checkout page is not loaded"
    expect(
        checkout_page.shipping_details_section_component.element
    ).to_be_visible(), "Shipping details section is not visible"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )


@pytest.mark.e2e
def test_e2e_proceed_to_single_page_checkout(
    config: Config,
    dataset: dict[str, Any],
    graphql_client: GraphQLClient,
    page: Page,
    auth: Auth,
):
    if config["CHECKOUT_MODE"] == "multi-step":
        pytest.skip("Checkout mode is a single-page")

    print(
        f"{os.linesep}Running E2E test to proceed to single-page checkout...", end=" "
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user = dataset["users"][0]

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

    expect(cart_page.page).to_have_url(cart_page.url), "Cart page is not loaded"
    expect(
        cart_page.shipping_details_section_component.shipping_method_selector
    ).to_be_visible(), "Shipping details section is not visible"
    expect(
        cart_page.payment_details_section_component.element
    ).to_be_visible(), "Payment details section is not visible"
    expect(
        cart_page.place_order_button
    ).to_be_visible(), "Place order button is not visible"

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )
