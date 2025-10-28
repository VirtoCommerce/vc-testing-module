import os
from typing import Any

import allure
import pytest
from gql import Client
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from fixtures.auth import Auth
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.e2e
@allure.title("Calculate shipping cost in single-page checkout (E2E)")
def test_e2e_shipping_cost_single_page_checkout(
    config: dict[str, Any],
    dataset: dict[str, Any],
    page: Page,
    auth: Auth,
    product_quantity_control: str,
    checkout_mode: str,
    graphql_client: Client,
):
    if checkout_mode == "multi-step":
        pytest.skip(
            "Checkout mode is a single-page, skipping test for multi-step checkout"
        )

    print(
        f"{os.linesep}Running E2E test to calculate shipping cost in single-page checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    auth.authenticate(dataset["users"][0]["userName"], config["users_password"])

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

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["defaultValue"]
    user = user_operations.get_me()
    cart = cart_operations.get_cart(
        config["store_id"],
        user["id"],
        currency,
        culture,
    )

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

    cart_page.clear_cart()
    auth.clear_token()


@pytest.mark.e2e
@allure.title("Calculate shipping cost in multi-step checkout (E2E)")
def test_e2e_shipping_cost_multi_step_checkout(
    config: dict[str, Any],
    dataset: dict[str, Any],
    page: Page,
    auth: Auth,
    product_quantity_control: str,
    checkout_mode: str,
    graphql_client: Client,
):
    if checkout_mode == "single-page":
        pytest.skip(
            "Checkout mode is a single-page, skipping test for multi-step checkout"
        )

    print(
        f"{os.linesep}Running E2E test to calculate shipping cost in multi-step checkout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    auth.authenticate(dataset["users"][0]["userName"], config["users_password"])

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

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["defaultValue"]
    user = user_operations.get_me()
    cart = cart_operations.get_cart(
        config["store_id"],
        user["id"],
        currency,
        culture,
    )

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

    cart_page.clear_cart()
    auth.clear_token()
