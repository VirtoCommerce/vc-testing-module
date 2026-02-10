import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Config
from tests_e2e.pages import CategoryPage


@pytest.mark.e2e
def test_e2e_category_scroll_to_product(
    config: Config, page: Page, dataset: dict[str, Any]
):
    print(
        f"{os.linesep}Running E2E test to scroll to product on category page...",
        end=" ",
    )

    page.set_viewport_size({"width": 1920, "height": 1080})

    category = dataset["categories"][0]
    product = dataset["products"][14]

    category_page = CategoryPage(config, page, category["seoInfos"][0]["semanticUrl"])
    category_page.navigate()

    category_page.view_switcher.switch_category_view("grid")

    product_card = category_page.scroll_to_product_card(product["code"])

    assert product_card is not None, "Product card is not found"
    expect(product_card.element, "Product card is not visible").to_be_visible()
