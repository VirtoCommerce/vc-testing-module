import os
from typing import Any, Dict

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.e2e
@allure.title("Category add to cart component viewport (E2E)")
def test_e2e_category_add_to_cart_component_viewport(
    config: Dict[str, Any],
    dataset: Dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    product_quantity_control: str,
):
    print(
        f"{os.linesep}Running E2E test to check category add to cart component viewport...",
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
        if product["id"] == "product-acme-laptop-asus-zenbook-a14-ux3407"
    )

    category_page = CategoryPage(
        config, page, category_to_browse["seoInfos"][0]["semanticUrl"]
    )
    category_page.navigate()
    category_page.view_switcher.switch_category_view("grid")

    product_card = category_page.get_product_card_by_sku(product_to_add_to_cart["code"])

    expect(product_card.element).to_be_visible(), "Product card is not visible"
    if product_quantity_control == "button":
        expect(
            product_card.add_to_cart_component.add_to_cart_text_button
        ).to_be_visible(), "Add to cart text button is not visible"
        expect(
            product_card.add_to_cart_component.add_to_cart_icon_button
        ).not_to_be_visible(), "Add to cart icon button is visible"

    page.set_viewport_size({"width": 800, "height": 600})

    if product_quantity_control == "button":
        expect(
            product_card.add_to_cart_text_button
        ).not_to_be_visible(), "Add to cart text button is visible"
        expect(
            product_card.add_to_cart_icon_button
        ).to_be_visible(), "Add to cart icon button is not visible"
