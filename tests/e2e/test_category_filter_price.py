import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import CategoryPage
from playwright.sync_api import Page, expect

_CATEGORY_PATH = "smartphones"
_EXPECTED_PRODUCTS_QTY = 4


@pytest.mark.e2e
@pytest.mark.range_filter_type("slider")
def test_category_filter_price_slider(global_settings: GlobalSettings, page: Page) -> None:
    category_page = CategoryPage(global_settings=global_settings, page=page, path=_CATEGORY_PATH)
    category_page.navigate()

    expect(category_page.price_slider_filter.root).to_be_visible()

    category_page.price_slider_filter.header.click()
    expect(category_page.price_slider_filter.content).to_be_visible()

    category_page.price_slider_filter.start_input.fill("1000")
    category_page.price_slider_filter.end_input.fill("2000")
    category_page.click_outside()

    expect(category_page.products_count_label).to_have_text(str(_EXPECTED_PRODUCTS_QTY))


@pytest.mark.e2e
@pytest.mark.range_filter_type("default")
def test_category_filter_price_checkboxes(global_settings: GlobalSettings, page: Page) -> None:
    category_page = CategoryPage(global_settings=global_settings, page=page, path=_CATEGORY_PATH)
    category_page.navigate()

    expect(category_page.price_checkboxes_filter.root).to_be_visible()

    category_page.price_checkboxes_filter.header.click()
    expect(category_page.price_checkboxes_filter.content).to_be_visible()

    category_page.price_checkboxes_filter.facet(facet_id="filter-price-[1000 TO 1300)").click()
    category_page.price_checkboxes_filter.facet(facet_id="filter-price-[1300 TO 1500)").click()
    category_page.price_checkboxes_filter.facet(facet_id="filter-price-[1500 TO 2000)").click()

    expect(category_page.products_count_label).to_have_text(str(_EXPECTED_PRODUCTS_QTY))
