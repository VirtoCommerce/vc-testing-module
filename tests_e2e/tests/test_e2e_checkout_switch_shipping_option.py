import os

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from test_data.test_category import TEST_CATEGORY_1
from test_data.test_product import TEST_PRODUCT_1
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage
from tests_e2e.pages.checkout_shipping_page import CheckoutShippingPage


@pytest.mark.ignore
@pytest.mark.e2e
@allure.title("Checkout - Switch shipping option (E2E)")
def test_e2e_checkout_switch_shipping_option(
    config: dict, page: Page, anonymous_catalog_requests: AnonymousCatalogRequests
):
    print(f"{os.linesep}Running E2E test to switch shipping option...", end=" ")

    anonymous_catalog_requests.toggle(True)

    page.set_viewport_size({"width": 1920, "height": 1080})

    category_page = CategoryPage(config, page, TEST_CATEGORY_1["seoPath"])
    category_page.navigate()

    product_card = category_page.get_product_card_by_sku(TEST_PRODUCT_1["sku"])
    product_card.quantity_input.fill("2")
    product_card.add_to_cart_text_button.click()

    cart_page = CartPage(config, page)
    cart_page.navigate()
    cart_page.checkout_button.click()

    checkout_shipping_page = CheckoutShippingPage(config, page)

    expect(page).to_have_url(
        checkout_shipping_page.url
    ), "Checkout shipping page is not loaded"
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
