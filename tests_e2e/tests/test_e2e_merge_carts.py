import allure, os, pytest
from playwright.sync_api import Page, expect
from fixtures.anonymous_catalog_requests_fixture import AnonymousCatalogRequests
from fixtures.requests_tracker_fixture import RequestsTracker
from tests_e2e.pages import cart_page
from tests_e2e.pages.category_page import CategoryPage
from test_data.test_category import TEST_CATEGORY_1
from test_data.test_product import TEST_PRODUCT_1
from tests_e2e.pages.sign_in_page import SignInPage
from tests_e2e.pages.cart_page import CartPage


@pytest.mark.e2e
@allure.title("Merge carts (E2E)")
def test_e2e_merge_carts(config: dict, page: Page, anonymous_catalog_requests: AnonymousCatalogRequests, requests_tracker: RequestsTracker):
    print(f"{os.linesep}Running E2E test to merge carts...", end=" ")

    anonymous_catalog_requests.toggle(True)

    page.set_viewport_size({"width": 1920, "height": 1080})

    category_page = CategoryPage(config, page, TEST_CATEGORY_1["seoPath"])
    category_page.navigate()

    product_card = category_page.get_product_card_by_sku(TEST_PRODUCT_1["sku"])
    product_card.quantity_input.fill("2")
    product_card.add_to_cart_text_button.click()

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(config["username"], config["password"])

    cart_page = CartPage(config, page)
    cart_page.navigate()

    assert not cart_page.is_empty, "Cart is empty after sign in"

    cart_page.clear_cart()
