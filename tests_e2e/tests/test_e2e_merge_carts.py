import os
import time
from typing import Any

import allure
import pytest
from playwright.sync_api import Page

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from fixtures.config import Config
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage
from tests_e2e.pages.sign_in_page import SignInPage


@pytest.mark.e2e
@allure.title("Merge carts (E2E)")
def test_e2e_merge_carts(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    product_quantity_control: str,
):
    print(f"{os.linesep}Running E2E test to merge carts...", end=" ")

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

    quantity_to_add = 2

    category_page.add_product_to_cart(product_to_add_to_cart["code"], quantity_to_add)

    user = dataset["users"][0]

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(user["userName"], config["USERS_PASSWORD"])

    cart_page = CartPage(config, page)
    cart_page.navigate()

    line_item = cart_page.get_line_item_by_sku(product_to_add_to_cart["code"])

    assert not cart_page.is_empty, "Cart is empty after sign in"
    assert (
        line_item.sku == product_to_add_to_cart["code"]
    ), f"Line item sku is not equal to product sku: {product_to_add_to_cart['code']}"
    assert str(
        line_item.quantity_stepper_component.quantity_input.input_value()
    ) == str(
        quantity_to_add
    ), f"Line item quantity is not equal to product quantity to add: {quantity_to_add}"

    cart_page.clear_cart()
