import os
import time
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage
from tests_e2e.pages.checkout_shipping_page import CheckoutShippingPage


@pytest.mark.e2e
@allure.title("Checkout multi-step - Switch shipping option (E2E)")
def test_e2e_checkout_multi_step_switch_shipping_option(
    config: dict[str, Any],
    dataset: dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    product_quantity_control: str,
    checkout_mode: str,
):
    if checkout_mode == "single-page":
        pytest.skip("Checkout mode is a multi-step")

    print(
        f"{os.linesep}Running E2E test to switch shipping option in multi-step checkout...",
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
        if product["id"] == "product-acme-laptop-asus-vivobook-16-x1607qa"
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

    cart_page = CartPage(config, page)
    cart_page.navigate()

    cart_page.checkout_button.click()

    checkout_shipping_page = CheckoutShippingPage(config, page)

    expect(page).to_have_url(
        checkout_shipping_page.url
    ), "Checkout shipping page is not loaded"
    expect(
        checkout_shipping_page.shipping_details_section_component.element
    ).to_be_visible(), "Shipping details section is not visible"
    expect(
        checkout_shipping_page.shipping_details_section_component.pickup_delivery_option_switcher
    ).to_be_visible(), "Pickup delivery option switcher is not visible"
    expect(
        checkout_shipping_page.shipping_details_section_component.shipping_delivery_option_switcher
    ).to_be_visible(), "Shipping delivery option switcher is not visible"

    checkout_shipping_page.shipping_details_section_component.switch_delivery_option(
        "pickup"
    )

    expect(
        checkout_shipping_page.shipping_details_section_component.pickup_point_section
    ).to_be_visible(), "Pickup point section is not visible"
    expect(
        checkout_shipping_page.shipping_details_section_component.shipping_method_selector
    ).not_to_be_visible(), "Shipping method selector is visible"

    checkout_shipping_page.shipping_details_section_component.switch_delivery_option(
        "shipping"
    )

    expect(
        checkout_shipping_page.shipping_details_section_component.pickup_point_section
    ).not_to_be_visible(), "Pickup point section is visible"
    expect(
        checkout_shipping_page.shipping_details_section_component.shipping_method_selector
    ).to_be_visible(), "Shipping method selector is not visible"


@pytest.mark.e2e
@allure.title("Checkout single-page - Switch shipping option (E2E)")
def test_e2e_checkout_single_page_switch_shipping_option(
    config: dict[str, Any],
    dataset: dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    product_quantity_control: str,
    checkout_mode: str,
):
    if checkout_mode == "multi-step":
        pytest.skip("Checkout mode is a single-page")

    print(
        f"{os.linesep}Running E2E test to switch shipping option in single-page checkout...",
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
        if product["id"] == "product-acme-laptop-asus-vivobook-16-x1607qa"
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

    cart_page = CartPage(config, page)
    cart_page.navigate()

    expect(page).to_have_url(cart_page.url), "Cart page is not loaded"
    expect(
        cart_page.shipping_details_section_component.element
    ).to_be_visible(), "Shipping details section is not visible"
    expect(
        cart_page.shipping_details_section_component.pickup_delivery_option_switcher
    ).to_be_visible(), "Pickup delivery option switcher is not visible"
    expect(
        cart_page.shipping_details_section_component.shipping_delivery_option_switcher
    ).to_be_visible(), "Shipping delivery option switcher is not visible"

    cart_page.shipping_details_section_component.switch_delivery_option("pickup")

    expect(
        cart_page.shipping_details_section_component.pickup_point_section
    ).to_be_visible(), "Pickup point section is not visible"
    expect(
        cart_page.shipping_details_section_component.shipping_method_selector
    ).not_to_be_visible(), "Shipping method selector is visible"

    cart_page.shipping_details_section_component.switch_delivery_option("shipping")

    expect(
        cart_page.shipping_details_section_component.pickup_point_section
    ).not_to_be_visible(), "Pickup point section is visible"
    expect(
        cart_page.shipping_details_section_component.shipping_method_selector
    ).to_be_visible(), "Shipping method selector is not visible"
