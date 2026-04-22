import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures.config import Config
from tests_e2e.pages.category_page import CategoryPage


@pytest.mark.e2e
def test_e2e_switch_category_grid_view(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
):
    print(f"{os.linesep}Running E2E test to switch category grid view...", end=" ")

    category = dataset["categories"][0]

    category_page = CategoryPage(config, page, category["seoInfos"][0]["semanticUrl"])
    category_page.navigate()
    category_page.view_switcher.switch_category_view("grid")

    expect(category_page.products_grid_view).to_be_visible(), "Products grid view is not visible"
    expect(category_page.products_list_view).not_to_be_visible(), "Products list view is visible"


@pytest.mark.e2e
def test_e2e_switch_category_list_view(
    config: Config,
    dataset: dict[str, Any],
    page: Page,
):
    print(f"{os.linesep}Running E2E test to switch category list view...", end=" ")

    category = dataset["categories"][0]

    category_page = CategoryPage(config, page, category["seoInfos"][0]["semanticUrl"])
    category_page.navigate()
    category_page.view_switcher.switch_category_view("list")

    expect(category_page.products_grid_view).not_to_be_visible(), "Products grid view is visible"
    expect(category_page.products_list_view).to_be_visible(), "Products list view is not visible"
