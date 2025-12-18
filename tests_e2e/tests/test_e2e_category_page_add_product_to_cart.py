import os
import time
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from fixtures.config import Config
from fixtures.requests_tracker import RequestsTracker
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.e2e
@allure.title("Add product to cart from category page with add to cart button (E2E)")
def test_e2e_category_add_product_to_cart_with_add_to_cart_button(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    requests_tracker: RequestsTracker,
    product_quantity_control: str,
):
    if product_quantity_control == "stepper":
        pytest.skip("Product quantity control is a stepper")

    print(
        f"{os.linesep}Running E2E test to add product to cart from category page with add to cart button...",
        end=" ",
    )

    product_quantity_to_add = "2"

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

    category_page.add_product_to_cart(
        product_to_add_to_cart["code"], product_quantity_to_add
    )

    cart_page = CartPage(config, page)
    cart_page.navigate()

    line_item = cart_page.get_line_item_by_sku(product_to_add_to_cart["code"])

    assert (
        line_item.sku == product_to_add_to_cart["code"]
    ), f"Line item sku is not equal to product sku: {product_to_add_to_cart['code']}"
    assert (
        str(line_item.add_to_cart_component.quantity_input.input_value())
        == product_quantity_to_add
    ), "Line item quantity is not equal to product quantity to add"

    cart_page.clear_cart()

    requests_tracker.wait_for_all_requests()

    assert cart_page.is_empty, "Cart is not empty after clearing"


@pytest.mark.e2e
@allure.title("Add product to cart from category page with quantity stepper (E2E)")
def test_e2e_category_add_product_to_cart_with_quantity_stepper(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    requests_tracker: RequestsTracker,
    product_quantity_control: str,
):
    if product_quantity_control == "button":
        pytest.skip("Product quantity control is add to cart button")

    print(
        f"{os.linesep}Running E2E test to add product to cart from category page with quantity stepper...",
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

    quantity_to_add = 2

    category_page = CategoryPage(
        config,
        page,
        category_to_browse["seoInfos"][0]["semanticUrl"],
        product_quantity_control,
    )
    category_page.navigate()
    category_page.add_product_to_cart(product_to_add_to_cart["code"], quantity_to_add)

    product_card = category_page.get_product_card_by_sku(product_to_add_to_cart["code"])

    expect(product_card.quantity_stepper_component.quantity_input).to_have_value(
        str(quantity_to_add)
    ), f"Quantity input is not equal to {quantity_to_add}"

    cart_page = CartPage(config, page)
    cart_page.navigate()

    line_item = cart_page.get_line_item_by_sku(product_to_add_to_cart["code"])

    assert (
        line_item.sku == product_to_add_to_cart["code"]
    ), f"Line item sku is not equal to product sku: {product_to_add_to_cart['code']}"
    assert str(
        line_item.quantity_stepper_component.quantity_input.input_value()
    ) == str(
        quantity_to_add
    ), f"Line item quantity is not equal to product quantity to add: {quantity_to_add}"

    cart_page.clear_cart()

    requests_tracker.wait_for_all_requests()

    assert cart_page.is_empty, "Cart is not empty after clearing"
