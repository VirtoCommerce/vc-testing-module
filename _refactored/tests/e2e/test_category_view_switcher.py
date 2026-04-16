import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings
from page_objects.pages import CategoryPage

_CATEGORY_PATH = "laptops"


@pytest.mark.e2e
def test_category_view_switcher(global_settings: GlobalSettings, page: Page) -> None:
    category_page = CategoryPage(
        global_settings=global_settings, page=page, path=_CATEGORY_PATH
    )
    category_page.navigate()
    expect(category_page.view_switcher.root).to_be_visible()

    category_page.view_switcher.grid_view_tab.click()
    expect(category_page.grid_view).to_be_visible()

    category_page.view_switcher.list_view_tab.click()
    expect(category_page.list_view).to_be_visible()
