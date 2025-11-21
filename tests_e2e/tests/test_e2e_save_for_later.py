import os
import time
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.requests_tracker import RequestsTracker
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage
from tests_e2e.pages.save_for_later_page import SaveForLaterPage
from tests_e2e.pages.sign_in_page import SignInPage


@pytest.mark.e2e
@allure.title("Add product to cart and save for later (E2E)")
def test_e2e_add_product_to_cart_and_save_for_later(
    config: dict[str, Any],
    dataset: dict[str, Any],
    page: Page,
    requests_tracker: RequestsTracker,
):
    print(
        f"{os.linesep}Running E2E test to add product to cart and save for later...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()

    sign_in_page.sign_in(dataset["users"][0]["userName"], config["users_password"])
    time.sleep(2)

    category_to_browse = next(
        category for category in dataset["categories"] if category["id"] == "category-acme-laptops"
    )

    product_to_add_to_cart_1 = next(
        product for product in dataset["products"] if product["id"] == "product-acme-laptop-hp-pavilion-16-ag0087nr"
    )

    product_to_add_to_cart_2 = next(
        product for product in dataset["products"] if product["id"] == "product-acme-laptop-asus-zenbook-a14-ux3407"
    )

    product_quantity = 2

    category_page = CategoryPage(config, page, category_to_browse["seoInfos"][0]["semanticUrl"])
    category_page.navigate()
    category_page.add_product_to_cart(product_to_add_to_cart_1["code"], product_quantity)
    category_page.add_product_to_cart(product_to_add_to_cart_2["code"], 1)
    requests_tracker.wait_for_all_requests()

    cart_page = CartPage(config, page)
    cart_page.navigate()

    expect(
        cart_page.get_line_item_by_sku(product_to_add_to_cart_1["code"]).quantity_stepper_component.quantity_input
    ).to_have_value(str(product_quantity)), f"Product quantity is not equal to {product_quantity}"

    cart_page.save_for_later(product_to_add_to_cart_1["code"])
    requests_tracker.wait_for_all_requests()

    # Verify that the first product is no longer in the cart
    removed_item = cart_page.get_line_item_by_sku(product_to_add_to_cart_1["code"])
    assert (
        removed_item is None
    ), f"Product {product_to_add_to_cart_1['code']} should not be in cart after saving for later"

    # Verify that the cart has only 1 item left
    assert (
        len(cart_page.line_items) == 1
    ), f"Cart should have 1 item after saving for later, but found {len(cart_page.line_items)}"

    # Verify that the second product is still in the cart
    remaining_item = cart_page.get_line_item_by_sku(product_to_add_to_cart_2["code"])
    expect(
        remaining_item.element
    ).to_be_visible(), f"Product {product_to_add_to_cart_2['code']} should still be in cart"

    save_for_later_page = SaveForLaterPage(page, config)
    save_for_later_page.navigate()

    saved_item = save_for_later_page.get_line_item_by_sku(product_to_add_to_cart_1["code"])
    expect(
        saved_item.element
    ).to_be_visible(), f"Product {product_to_add_to_cart_1['code']} should be in saved for later"

    save_for_later_page.remove_line_item(product_to_add_to_cart_1["code"])
    requests_tracker.wait_for_all_requests()

    cart_page.navigate()
    cart_page.clear_cart()


@pytest.mark.e2e
@allure.title("Move product from saved for later to cart (E2E)")
def test_e2e_move_product_from_saved_for_later_to_cart(
    config: dict[str, Any],
    dataset: dict[str, Any],
    page: Page,
    requests_tracker: RequestsTracker,
):
    print(
        f"{os.linesep}Running E2E test to move product from saved for later to cart...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()

    sign_in_page.sign_in(dataset["users"][0]["userName"], config["users_password"])
    time.sleep(2)

    category_to_browse = next(
        category for category in dataset["categories"] if category["id"] == "category-acme-laptops"
    )

    product_to_add_to_cart = next(
        product for product in dataset["products"] if product["id"] == "product-acme-laptop-hp-pavilion-16-ag0087nr"
    )

    product_quantity = 3

    category_page = CategoryPage(config, page, category_to_browse["seoInfos"][0]["semanticUrl"])
    category_page.navigate()
    category_page.add_product_to_cart(product_to_add_to_cart["code"], product_quantity)
    requests_tracker.wait_for_all_requests()

    cart_page = CartPage(config, page)
    cart_page.navigate()

    cart_page.save_for_later(product_to_add_to_cart["code"])
    requests_tracker.wait_for_all_requests()

    save_for_later_page = SaveForLaterPage(page, config)
    save_for_later_page.navigate()

    saved_item = save_for_later_page.get_line_item_by_sku(product_to_add_to_cart["code"])
    expect(saved_item.element).to_be_visible(), f"Product {product_to_add_to_cart['code']} should be in saved for later"

    expect(saved_item.add_to_cart_component.quantity_input).to_have_value(
        str(product_quantity)
    ), f"Product quantity is not equal to {product_quantity}"

    saved_item.add_to_cart_component.add_to_cart_text_button.click()
    requests_tracker.wait_for_all_requests()

    cart_page.navigate()
    expect(
        cart_page.get_line_item_by_sku(product_to_add_to_cart["code"]).element
    ).to_be_visible(), f"Product {product_to_add_to_cart['code']} should be in cart"
    expect(
        cart_page.get_line_item_by_sku(product_to_add_to_cart["code"]).quantity_stepper_component.quantity_input
    ).to_have_value(str(product_quantity)), f"Product quantity is not equal to {product_quantity}"

    cart_page.clear_cart()

    save_for_later_page.navigate()
    save_for_later_page.remove_line_item(product_to_add_to_cart["code"])
    requests_tracker.wait_for_all_requests()

    assert save_for_later_page.is_empty, "Saved for later page is not empty after removing product"
