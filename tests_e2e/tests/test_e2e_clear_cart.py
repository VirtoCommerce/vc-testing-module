import os
import time
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from fixtures.config import Config
from fixtures.requests_tracker import RequestsTracker
from tests_e2e.components.clear_cart_modal_component import ClearCartModalComponent
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.e2e
@allure.title("Clear cart (E2E)")
def test_e2e_clear_cart(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    requests_tracker: RequestsTracker,
    product_quantity_control: str,
):
    print(f"{os.linesep}Running E2E test to clear cart...", end=" ")

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

    category_page.add_product_to_cart(product_to_add_to_cart["code"], 2)

    cart_page = CartPage(config, page)
    cart_page.navigate()
    cart_page.clear_cart_button.click()

    clear_cart_modal = ClearCartModalComponent(
        page.locator("[data-test-id='clear-cart-modal']")
    )

    expect(clear_cart_modal.element).to_be_visible(), "Clear cart modal is not visible"

    clear_cart_modal.no_button.click()

    expect(clear_cart_modal.element).not_to_be_visible(), "Clear cart modal is visible"

    cart_page.clear_cart()

    requests_tracker.wait_for_all_requests()

    assert cart_page.is_empty, "Cart is not empty after clearing"
