import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Config
from tests_e2e.pages import CategoryPage


@pytest.mark.e2e
@pytest.mark.range_filter("slider")
def test_e2e_category_price_range_filter_slider(
    config: Config,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to check category price range filter slider...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    category = dataset["categories"][0]

    category_page = CategoryPage(config, page, category["seoInfos"][0]["semanticUrl"])
    category_page.navigate()

    expect(category_page.price_filter_slider.element).to_be_visible()

    category_page.price_filter_slider.click_header()

    expect(category_page.price_filter_slider.lower_handler).to_be_visible()
    expect(category_page.price_filter_slider.upper_handler).to_be_visible()

    category_page.price_filter_slider.lower_input.fill("1000")
    category_page.price_filter_slider.upper_input.fill("2000")

    page.locator("body").click()

    category_page.products_count_locator.wait_for(state="visible")
    page.wait_for_timeout(2000)

    assert category_page.products_count == 13, "Products count is not equal to 13"


@pytest.mark.e2e
@pytest.mark.range_filter("default")
def test_e2e_category_price_range_filter_default(
    config: Config,
    page: Page,
    dataset: dict[str, Any],
):

    print(
        f"{os.linesep}Running E2E test to check default category price range filter...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    category = dataset["categories"][0]

    category_page = CategoryPage(config, page, category["seoInfos"][0]["semanticUrl"])
    category_page.navigate()

    expect(category_page.price_filter_facets.element).to_be_visible()

    category_page.price_filter_facets.click_header()

    category_page.price_filter_facets.click_facet_item("filter-price-[1000 TO 1300)")
    category_page.price_filter_facets.click_facet_item("filter-price-[1300 TO 1500)")
    category_page.price_filter_facets.click_facet_item("filter-price-[1500 TO 2000)")

    category_page.products_count_locator.wait_for(state="visible")

    assert category_page.products_count == 13, "Products count is not equal to 13"
