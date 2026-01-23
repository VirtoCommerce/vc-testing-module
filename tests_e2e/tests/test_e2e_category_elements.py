import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Config
from tests_e2e.pages import CategoryPage


@pytest.mark.e2e
def test_e2e_category_elements(
    config: Config,
    page: Page,
    dataset: dict[str, Any],
):
    print(f"{os.linesep}Running E2E test to check category elements...", end=" ")

    category = dataset["categories"][0]

    category_page = CategoryPage(config, page, category["seoInfos"][0]["semanticUrl"])
    category_page.navigate()
    category_page.view_switcher.switch_category_view("grid")

    expect(category_page.view_switcher.element).to_be_visible()
    expect(category_page.products_grid_view).to_be_visible()
    expect(category_page.products_list_view).not_to_be_visible()
