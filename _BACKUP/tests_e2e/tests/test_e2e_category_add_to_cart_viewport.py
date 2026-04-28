import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Config
from tests_e2e.pages import CategoryPage


@pytest.mark.e2e
@pytest.mark.quantity_control("stepper")
def test_e2e_category_add_to_cart_component_viewport_stepper(
    config: Config,
    page: Page,
    dataset: dict[str, Any],
):
    print(
        f"{os.linesep}Running E2E test to check category add to cart stepper component viewport...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    category = dataset["categories"][0]
    product = dataset["products"][1]

    category_page = CategoryPage(config, page, category["seoInfos"][0]["semanticUrl"])
    category_page.navigate()

    category_page.view_switcher.switch_category_view("grid")

    product_card = category_page.get_product_card_by_sku_grid(product["code"])

    expect(product_card.element).to_be_visible(), "Product card is not visible"

    expect(product_card.quantity_stepper_component.element).to_be_visible(), "Quantity stepper component is not visible"


@pytest.mark.e2e
@pytest.mark.quantity_control("button")
def test_e2e_category_add_to_cart_component_viewport_button(
    config: Config,
    page: Page,
    dataset: dict[str, Any],
):
    print(
        f"{os.linesep}Running E2E test to check category add to cart button component viewport...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    category = dataset["categories"][0]
    product = dataset["products"][1]

    category_page = CategoryPage(config, page, category["seoInfos"][0]["semanticUrl"])
    category_page.navigate()

    category_page.view_switcher.switch_category_view("grid")

    product_card = category_page.get_product_card_by_sku_grid(product["code"])

    expect(product_card.element).to_be_visible(), "Product card is not visible"

    expect(
        product_card.add_to_cart_component.add_to_cart_text_button
    ).to_be_visible(), "Add to cart text button is not visible"
    expect(
        product_card.add_to_cart_component.add_to_cart_icon_button
    ).not_to_be_visible(), "Add to cart icon button is visible"

    page.set_viewport_size({"width": 800, "height": 600})

    expect(
        product_card.add_to_cart_component.add_to_cart_text_button
    ).not_to_be_visible(), "Add to cart text button is visible"
    expect(
        product_card.add_to_cart_component.add_to_cart_icon_button
    ).to_be_visible(), "Add to cart icon button is not visible"
