import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.e2e
@allure.title("Switch category grid view (E2E)")
def test_e2e_switch_category_grid_view(
    config: dict[str, Any],
    dataset: dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
):
    print(f"{os.linesep}Running E2E test to switch category grid view...", end=" ")

    anonymous_catalog_requests.toggle(True)

    category_to_browse = next(
        category
        for category in dataset["categories"]
        if category["id"] == "category-acme-laptops"
    )

    category_page = CategoryPage(
        config, page, category_to_browse["seoInfos"][0]["semanticUrl"]
    )
    category_page.navigate()
    category_page.view_switcher.switch_category_view("grid")

    expect(
        category_page.products_grid_view
    ).to_be_visible(), "Products grid view is not visible"
    expect(
        category_page.products_list_view
    ).not_to_be_visible(), "Products list view is visible"


@pytest.mark.e2e
@allure.title("Switch category list view (E2E)")
def test_e2e_switch_category_list_view(
    config: dict[str, Any],
    dataset: dict[str, Any],
    page: Page,
    anonymous_catalog_requests: AnonymousCatalogRequests,
):
    print(f"{os.linesep}Running E2E test to switch category list view...", end=" ")

    anonymous_catalog_requests.toggle(True)

    category_to_browse = next(
        category
        for category in dataset["categories"]
        if category["id"] == "category-acme-laptops"
    )

    category_page = CategoryPage(
        config, page, category_to_browse["seoInfos"][0]["semanticUrl"]
    )
    category_page.navigate()
    category_page.view_switcher.switch_category_view("list")

    expect(
        category_page.products_grid_view
    ).not_to_be_visible(), "Products grid view is visible"
    expect(
        category_page.products_list_view
    ).to_be_visible(), "Products list view is not visible"
