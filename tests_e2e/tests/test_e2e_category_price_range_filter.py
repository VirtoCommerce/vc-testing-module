import time
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from fixtures.config import Config
from fixtures.requests_tracker import RequestsTracker
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.e2e
def test_e2e_category_price_range_filter_slider(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    product_quantity_control: str,
    range_filter_type: str,
    requests_tracker: RequestsTracker,
):
    if range_filter_type == "default":
        pytest.skip("Range filter type is not supported for this test")

    anonymous_catalog_requests.toggle(True)
    page.set_viewport_size({"width": 1920, "height": 1080})

    category_to_browse = next(
        category
        for category in dataset["categories"]
        if category["id"] == "category-acme-laptops"
    )

    category_page = CategoryPage(
        config,
        page,
        category_to_browse["seoInfos"][0]["semanticUrl"],
        product_quantity_control,
    )
    category_page.navigate()

    expect(category_page.price_filter_slider.element).to_be_visible()

    category_page.price_filter_slider.click_header()

    expect(category_page.price_filter_slider.lower_handler).to_be_visible()
    expect(category_page.price_filter_slider.upper_handler).to_be_visible()

    category_page.price_filter_slider.lower_input.fill("1000")
    category_page.price_filter_slider.upper_input.fill("2000")

    page.locator("body").click()
    requests_tracker.wait_for_all_requests()

    assert category_page.products_count == 13, "Products count is not equal to 13"


@pytest.mark.e2e
def test_e2e_category_price_range_filter_checkboxes(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    product_quantity_control: str,
    range_filter_type: str,
    requests_tracker: RequestsTracker,
):
    if range_filter_type == "slider":
        pytest.skip("Range filter type is not supported for this test")

    anonymous_catalog_requests.toggle(True)
    page.set_viewport_size({"width": 1920, "height": 1080})

    category_to_browse = next(
        category
        for category in dataset["categories"]
        if category["id"] == "category-acme-laptops"
    )

    category_page = CategoryPage(
        config,
        page,
        category_to_browse["seoInfos"][0]["semanticUrl"],
        product_quantity_control,
    )
    category_page.navigate()

    expect(category_page.price_filter_facets.element).to_be_visible()

    category_page.price_filter_facets.click_header()

    category_page.price_filter_facets.click_facet_item("filter-price-[1000 TO 1300)")
    category_page.price_filter_facets.click_facet_item("filter-price-[1300 TO 1500)")
    category_page.price_filter_facets.click_facet_item("filter-price-[1500 TO 2000)")

    time.sleep(2)

    assert category_page.products_count == 13, "Products count is not equal to 13"
