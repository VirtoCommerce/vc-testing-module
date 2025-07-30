import allure, os, pytest
from playwright.sync_api import Page, expect
from tests_e2e.pages.category_page import CategoryPage
from fixtures.anonymous_catalog_requests_fixture import AnonymousCatalogRequests
from test_data.test_category import TEST_CATEGORY_1
from test_data.test_product import TEST_PRODUCT_1


@pytest.mark.e2e
@allure.title("Category add to cart component viewport (E2E)")
def test_e2e_category_add_to_cart_component_viewport(config: dict, page: Page, anonymous_catalog_requests: AnonymousCatalogRequests):
    print(f"{os.linesep}Running E2E test to check category add to cart component viewport...", end=" ")

    anonymous_catalog_requests.toggle(True)

    page.set_viewport_size({"width": 1920, "height": 1080})

    category_page = CategoryPage(config, page, TEST_CATEGORY_1["seoPath"])
    category_page.navigate()
    category_page.view_switcher.switch_category_view("grid")

    product_card = category_page.get_product_card_by_sku(TEST_PRODUCT_1["sku"])

    expect(product_card.element).to_be_visible(), "Product card is not visible"
    expect(product_card.add_to_cart_text_button).to_be_visible(), "Add to cart text button is not visible"
    expect(product_card.add_to_cart_icon_button).not_to_be_visible(), "Add to cart icon button is visible"

    page.set_viewport_size({"width": 800, "height": 600})

    expect(product_card.add_to_cart_text_button).not_to_be_visible(), "Add to cart text button is visible"
    expect(product_card.add_to_cart_icon_button).to_be_visible(), "Add to cart icon button is not visible"
