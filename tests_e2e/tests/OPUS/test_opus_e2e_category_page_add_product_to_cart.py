import os
import time
from typing import Any, Dict

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from fixtures.requests_tracker import RequestsTracker
from tests_e2e.pages.sign_in_page import SignInPage
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage
from test_data.test_category import TEST_CATEGORY_1
from test_data.test_product import TEST_PRODUCT_1

@pytest.mark.e2e
@allure.title("Add product to cart from category page with add to cart button (E2E)")
def test_e2e_category_add_product_to_cart_with_add_to_cartbutton(
    config: Dict[str, Any],
    dataset: Dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    requests_tracker: RequestsTracker,
    product_quantity_control: str,
):

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(config["username"], config["password"])

    if product_quantity_control == "stepper":
        pytest.skip("Product quantity control is a stepper")

    print(
        f"{os.linesep}Running E2E test to add product to cart from category page with add to cart button...",
        end=" ",
    )
    
    product_quantity_to_add = "2"

    anonymous_catalog_requests.toggle(False)

    category_to_browse = TEST_CATEGORY_1["seoPath"]
    product_to_add_to_cart = TEST_PRODUCT_1

    category_page = CategoryPage(
        config, page, category_to_browse
    )

    category_page.navigate()

    expect(page).to_have_url(
        f"{config['frontend_base_url']}/{category_to_browse}"
    )
    
    product_card = category_page.get_product_card_by_sku(product_to_add_to_cart["sku"])
    product_card.add_to_cart_component.quantity_input.fill(product_quantity_to_add)
    product_card.add_to_cart_component.add_to_cart_text_button.click()

    cart_page = CartPage(config, page)
    cart_page.navigate()

    line_item = cart_page.get_line_item_by_sku(product_to_add_to_cart["sku"])

    assert (
        line_item.sku == product_to_add_to_cart["sku"]
    ), f"Line item sku is not equal to product sku: {product_to_add_to_cart['sku']}"
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
    config: Dict[str, Any],
    dataset: Dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    requests_tracker: RequestsTracker,
    product_quantity_control: str,
):


    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(config["username"], config["password"])

    if product_quantity_control == "button":
        pytest.skip("Product quantity control is add to cart button")

    print(
        f"{os.linesep}Running E2E test to add product to cart from category page with quantity stepper...",
        end=" ",
    )

    anonymous_catalog_requests.toggle(False)

    category_to_browse = TEST_CATEGORY_1["seoPath"]

    category_page = CategoryPage(
        config, page, category_to_browse
    )
    category_page.navigate()
    assert category_page.results_number > 10000, "No results found on the category page"

    expect(page).to_have_url(
        f"{config['frontend_base_url']}/{category_to_browse}"
    )
    product_card = category_page.get_first_product_card()
    assert product_card is not None, "No product cards found on the category page"
    
    product_sku = product_card.sku
    
    product_card.quantity_stepper_component.increment_button.click()

    expect(product_card.quantity_stepper_component.quantity_input).to_have_value(
        "1"
    ), "Quantity input is not equal to 1"

    time.sleep(2)

    cart_page = CartPage(config, page)
    cart_page.navigate()

    line_item = cart_page.get_line_item_by_sku(product_sku)

    assert (
        line_item.sku == product_sku
    ), f"Line item sku is not equal to product sku: {product_sku}"
    assert (
        str(line_item.quantity_stepper_component.quantity_input.input_value()) == "1"
    ), "Line item quantity is not equal to product quantity to add"

    cart_page.clear_cart()

    requests_tracker.wait_for_all_requests()

    assert cart_page.is_empty, "Cart is not empty after clearing"