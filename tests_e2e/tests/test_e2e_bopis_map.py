import os
import time
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from tests_e2e.components.address_filter_component import AddressFilterComponent
from tests_e2e.components.edit_address_modal_component import EditAddressModalComponent
from fixtures.requests_tracker import RequestsTracker
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.e2e
@allure.title("BOPIS map test (E2E)")
def test_e2e_remove_cart_item(
    config: dict[str, Any],
    dataset: dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    requests_tracker: RequestsTracker,
    product_quantity_control: str,
):
    print(f"{os.linesep}Running E2E test of BOPIS map...", end=" ")

    anonymous_catalog_requests.toggle(True)

    page.set_viewport_size({"width": 1920, "height": 1080})

    category_to_browse = next(
        category for category in dataset["categories"] if category["id"] == "category-acme-laptops"
    )
    product_to_add_to_cart = next(
        product for product in dataset["products"] if product["id"] == "product-acme-laptop-hp-pavilion-16-ag0087nr"
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

    cart_page.shipping_details_section_component.address_selector_component.select_address_button.click()

    address_filter = AddressFilterComponent(page.locator("[data-test-id='edit-address-modal']"))

    expect(address_filter.element).to_be_visible()
