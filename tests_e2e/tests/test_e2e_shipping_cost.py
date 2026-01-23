import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import CartPage, CheckoutShippingPage


@pytest.mark.e2e
def test_e2e_shipping_cost_single_page_checkout(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    auth: Auth,
    graphql_client: GraphQLClient,
):
    if config["CHECKOUT_MODE"] == "multi-step":
        pytest.skip(
            "Checkout mode is a single-page, skipping test for multi-step checkout"
        )

    print(
        f"{os.linesep}Running E2E test to calculate shipping cost in single-page checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    product = dataset["products"][1]

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"], page)

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

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    ground_shipping_method = next(
        shipping_method
        for shipping_method in cart["availableShippingMethods"]
        if shipping_method["code"] == "FixedRate"
        and shipping_method["optionName"] == "Ground"
    )
    air_shipping_method = next(
        shipping_method
        for shipping_method in cart["availableShippingMethods"]
        if shipping_method["code"] == "FixedRate"
        and shipping_method["optionName"] == "Air"
    )
    bopis_shipping_method = next(
        shipping_method
        for shipping_method in cart["availableShippingMethods"]
        if shipping_method["code"] == "BuyOnlinePickupInStore"
    )

    cart_page.shipping_details_section_component.shipping_delivery_option_switcher.click()
    cart_page.shipping_details_section_component.select_shipping_method(
        f"{ground_shipping_method['code']}_{ground_shipping_method['optionName']}"
    )

    expect(cart_page.order_summary_component.cart_shipping_total_label).to_have_text(
        ground_shipping_method["price"]["formattedAmount"]
    )

    cart_page.shipping_details_section_component.select_shipping_method(
        f"{air_shipping_method['code']}_{air_shipping_method['optionName']}"
    )

    expect(cart_page.order_summary_component.cart_shipping_total_label).to_have_text(
        air_shipping_method["price"]["formattedAmount"]
    )

    cart_page.shipping_details_section_component.pickup_delivery_option_switcher.click()

    expect(cart_page.order_summary_component.cart_shipping_total_label).to_have_text(
        bopis_shipping_method["price"]["formattedAmount"]
    )

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )


@pytest.mark.e2e
def test_e2e_shipping_cost_multi_step_checkout(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    auth: Auth,
    graphql_client: GraphQLClient,
):
    if config["CHECKOUT_MODE"] == "single-page":
        pytest.skip(
            "Checkout mode is a single-page, skipping test for multi-step checkout"
        )

    print(
        f"{os.linesep}Running E2E test to calculate shipping cost in multi-step checkout...",
        end=" ",
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

    ground_shipping_method = next(
        shipping_method
        for shipping_method in cart["availableShippingMethods"]
        if shipping_method["code"] == "FixedRate"
        and shipping_method["optionName"] == "Ground"
    )
    air_shipping_method = next(
        shipping_method
        for shipping_method in cart["availableShippingMethods"]
        if shipping_method["code"] == "FixedRate"
        and shipping_method["optionName"] == "Air"
    )
    bopis_shipping_method = next(
        shipping_method
        for shipping_method in cart["availableShippingMethods"]
        if shipping_method["code"] == "BuyOnlinePickupInStore"
    )

    checkout_shipping_page.shipping_details_section_component.shipping_delivery_option_switcher.click()
    checkout_shipping_page.shipping_details_section_component.select_shipping_method(
        f"{ground_shipping_method['code']}_{ground_shipping_method['optionName']}"
    )

    expect(
        checkout_shipping_page.order_summary_component.cart_shipping_total_label
    ).to_have_text(ground_shipping_method["price"]["formattedAmount"])

    checkout_shipping_page.shipping_details_section_component.select_shipping_method(
        f"{air_shipping_method['code']}_{air_shipping_method['optionName']}"
    )

    expect(
        checkout_shipping_page.order_summary_component.cart_shipping_total_label
    ).to_have_text(air_shipping_method["price"]["formattedAmount"])

    checkout_shipping_page.shipping_details_section_component.pickup_delivery_option_switcher.click()

    expect(
        checkout_shipping_page.order_summary_component.cart_shipping_total_label
    ).to_have_text(bopis_shipping_method["price"]["formattedAmount"])

    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )
