import os

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures import AnonymousCatalogRequests, RequestsTracker
from test_data.test_category import TEST_CATEGORY_1
from test_data.test_product import TEST_PRODUCT_1
from tests_e2e.components.clear_cart_modal_component import ClearCartModalComponent
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.ignore
@pytest.mark.e2e
@allure.title("Clear cart (E2E)")
def test_e2e_clear_cart(
    config: dict,
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    requests_tracker: RequestsTracker,
):
    print(f"{os.linesep}Running E2E test to clear cart...", end=" ")

    anonymous_catalog_requests.toggle(True)

    page.set_viewport_size({"width": 1920, "height": 1080})

    category_page = CategoryPage(config, page, TEST_CATEGORY_1["seoPath"])
    cart_page = CartPage(config, page)
    category_page.navigate()

    product_card = category_page.get_product_card_by_sku(TEST_PRODUCT_1["sku"])
    product_card.quantity_input.fill("2")
    product_card.add_to_cart_text_button.click()

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
