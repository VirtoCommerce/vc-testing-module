import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import CategoryPage
from playwright.sync_api import Page, expect

_CATEGORY_PATH = "smartphones"


@pytest.mark.e2e
@pytest.mark.flaky(retries=4, delay=10)
@allure.feature("Category / View switcher (E2E)")
@allure.title("Toggle between grid and list views on the category page")
def test_category_view_switcher(global_settings: GlobalSettings, page: Page) -> None:
    category_page = CategoryPage(global_settings=global_settings, page=page, path=_CATEGORY_PATH)

    with allure.step(f"Navigate to category '{_CATEGORY_PATH}'"):
        category_page.navigate()
        expect(category_page.view_switcher.root).to_be_visible()

    with allure.step("Switch to grid view and verify"):
        category_page.view_switcher.grid_view_tab.click()
        expect(category_page.grid_view).to_be_visible()

    with allure.step("Switch to list view and verify"):
        category_page.view_switcher.list_view_tab.click()
        expect(category_page.list_view).to_be_visible()
