import os

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests_fixture import AnonymousCatalogRequests
from fixtures.requests_tracker_fixture import RequestsTracker
from test_data.test_category import TEST_CATEGORY_1
from test_data.test_product import TEST_PRODUCT_1
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.e2e
@allure.title("Add product to cart from category page (E2E)")
def test_e2e_category_add_product_to_cart(
    config: dict,
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    requests_tracker: RequestsTracker,
):
    print(
        f"{os.linesep}Running E2E test to add product to cart from category page...",
        end=" ",
    )

    product_quantity_to_add = "2"

    anonymous_catalog_requests.toggle(True)

    page.set_viewport_size({"width": 1920, "height": 1080})

    category_page = CategoryPage(config, page, TEST_CATEGORY_1["seoPath"])
    category_page.navigate()

    expect(page).to_have_url(f"{config['base_url']}/{TEST_CATEGORY_1['seoPath']}")

    product_card = category_page.get_product_card_by_sku(TEST_PRODUCT_1["sku"])
    product_card.quantity_input.fill(product_quantity_to_add)
    product_card.add_to_cart_text_button.click()

    cart_page = CartPage(config, page)
    cart_page.navigate()

    line_item = cart_page.get_line_item_by_sku(TEST_PRODUCT_1["sku"])

    assert (
        line_item.sku == TEST_PRODUCT_1["sku"]
    ), f"Line item sku is not equal to product sku: {TEST_PRODUCT_1['sku']}"
    assert (
        str(line_item.quantity_input.input_value()) == product_quantity_to_add
    ), "Line item quantity is not equal to product quantity to add"

    cart_page.clear_cart()

    requests_tracker.wait_for_all_requests()

    assert cart_page.is_empty, "Cart is not empty after clearing"
