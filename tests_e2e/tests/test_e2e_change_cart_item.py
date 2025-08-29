import os

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures import AnonymousCatalogRequests, RequestsTracker
from test_data.test_category import TEST_CATEGORY_1
from test_data.test_product import TEST_PRODUCT_1
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.e2e
@allure.title("Change cart item (E2E)")
def test_e2e_change_cart_item(
    config: dict,
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    requests_tracker: RequestsTracker,
):
    print(f"{os.linesep}Running E2E test to change cart item...", end=" ")

    anonymous_catalog_requests.toggle(True)

    page.set_viewport_size({"width": 1920, "height": 1080})

    category_page = CategoryPage(config, page, TEST_CATEGORY_1["seoPath"])
    category_page.navigate()

    product_card = category_page.get_product_card_by_sku(TEST_PRODUCT_1["sku"])
    product_card.quantity_input.fill("2")
    product_card.add_to_cart_text_button.click()

    cart_page = CartPage(config, page)
    cart_page.navigate()

    line_item = cart_page.get_line_item_by_sku(TEST_PRODUCT_1["sku"])
    line_item.quantity_input.fill("3")

    requests_tracker.wait_for_all_requests()

    expect(line_item.quantity_input).to_have_value("3")
