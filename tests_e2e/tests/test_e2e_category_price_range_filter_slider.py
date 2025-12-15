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
    requests_tracker: RequestsTracker,
):
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

    expect(category_page.price_filter.element).to_be_visible()

    category_page.price_filter.click_header()

    expect(category_page.price_filter.lower_handler).to_be_visible()
    expect(category_page.price_filter.upper_handler).to_be_visible()

    category_page.price_filter.lower_input.fill("1200")
    category_page.price_filter.upper_input.fill("3000")

    page.locator("body").click()
    requests_tracker.wait_for_all_requests()

    assert category_page.products_count == 11, "Products count is not equal to 11"
