import os
import time
from typing import Any

import allure
import pytest
from playwright.sync_api import Page

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage
from tests_e2e.pages.sign_in_page import SignInPage


@pytest.mark.e2e
@allure.title("Merge carts (E2E)")
def test_e2e_merge_carts(
    config: dict[str, Any],
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
        config, page, category_to_browse["seoInfos"][0]["semanticUrl"]
    )
    category_page.navigate()

    product_card = category_page.get_product_card_by_sku(product_to_add_to_cart["code"])
    if product_quantity_control == "stepper":
        product_card.quantity_stepper_component.increment_button.click()
        product_card.quantity_stepper_component.increment_button.click()
    elif product_quantity_control == "button":
        product_card.add_to_cart_component.quantity_input.fill("2")
        product_card.add_to_cart_component.add_to_cart_text_button.click()

    time.sleep(2)

    user = dataset["users"][0]

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(user["userName"], config["users_password"])

    cart_page = CartPage(config, page)
    cart_page.navigate()

    assert not cart_page.is_empty, "Cart is empty after sign in"

    cart_page.clear_cart()
