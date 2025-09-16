import os
from typing import Any, Dict

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from fixtures.requests_tracker import RequestsTracker
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.ignore
@pytest.mark.e2e
@allure.title("Change cart item (E2E)")
def test_e2e_change_cart_item(
    config: Dict[str, Any],
    dataset: Dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    requests_tracker: RequestsTracker,
    product_quantity_control: str,
):
    print(f"{os.linesep}Running E2E test to change cart item...", end=" ")

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
        if product["id"] == "product-acme-laptop-asus-zenbook-a14-ux3407"
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

    cart_page = CartPage(config, page)
    cart_page.navigate()

    line_item = cart_page.get_line_item_by_sku(product_to_add_to_cart["code"])
    if product_quantity_control == "stepper":
        line_item.quantity_stepper_component.increment_button.click()
    elif product_quantity_control == "button":
        line_item.add_to_cart_component.quantity_input.fill("3")

    requests_tracker.wait_for_all_requests()

    if product_quantity_control == "stepper":
        expect(line_item.quantity_stepper_component.quantity_input).to_have_value("3")
    elif product_quantity_control == "button":
        expect(line_item.add_to_cart_component.quantity_input).to_have_value("3")
