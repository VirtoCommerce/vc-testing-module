import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from fixtures.config import Config
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.e2e
@allure.title("Category elements (E2E)")
def test_e2e_category_elements(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
    product_quantity_control: str,
):
    print(f"{os.linesep}Running E2E test to check category elements...", end=" ")

    anonymous_catalog_requests.toggle(True)

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
    category_page.view_switcher.switch_category_view("grid")

    expect(category_page.view_switcher.element).to_be_visible()
    expect(category_page.products_grid_view).to_be_visible()
    expect(category_page.products_list_view).not_to_be_visible()
