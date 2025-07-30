import allure, os, pytest
from playwright.sync_api import Page, expect
from tests_e2e.pages.category_page import CategoryPage
from fixtures.anonymous_catalog_requests_fixture import AnonymousCatalogRequests
from test_data.test_category import TEST_CATEGORY_1


@pytest.mark.e2e
@allure.title("Category elements (E2E)")
def test_e2e_category_elements(config: dict, page: Page, anonymous_catalog_requests: AnonymousCatalogRequests):
    print(f"{os.linesep}Running E2E test to check category elements...", end=" ")

    anonymous_catalog_requests.toggle(True)

    category_page = CategoryPage(config, page, TEST_CATEGORY_1["seoPath"])
    category_page.navigate()
    category_page.view_switcher.switch_category_view("grid")

    expect(category_page.page).to_have_url(category_page.url)
    expect(category_page.view_switcher.element).to_be_visible()
    expect(category_page.products_grid_view).to_be_visible()
    expect(category_page.products_list_view).not_to_be_visible()
