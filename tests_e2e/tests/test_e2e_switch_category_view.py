import os

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.anonymous_catalog_requests import AnonymousCatalogRequests
from test_data.test_category import TEST_CATEGORY_1
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.e2e
@allure.title("Switch category grid view (E2E)")
def test_e2e_switch_category_grid_view(
    config: dict, page: Page, anonymous_catalog_requests: AnonymousCatalogRequests
):
    print(f"{os.linesep}Running E2E test to switch category grid view...", end=" ")

    anonymous_catalog_requests.toggle(True)

    category_page = CategoryPage(config, page, TEST_CATEGORY_1["seoPath"])
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
    config: dict, page: Page, anonymous_catalog_requests: AnonymousCatalogRequests
):
    print(f"{os.linesep}Running E2E test to switch category list view...", end=" ")

    anonymous_catalog_requests.toggle(True)

    category_page = CategoryPage(config, page, TEST_CATEGORY_1["seoPath"])
    category_page.navigate()
    category_page.view_switcher.switch_category_view("list")

    expect(
        category_page.products_grid_view
    ).not_to_be_visible(), "Products grid view is visible"
    expect(
        category_page.products_list_view
    ).to_be_visible(), "Products list view is not visible"
