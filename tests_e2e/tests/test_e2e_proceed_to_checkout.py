import allure, os, pytest
from playwright.sync_api import Page, expect
from fixtures.requests_tracker_fixture import RequestsTracker
from tests_e2e.pages.sign_in_page import SignInPage
from tests_e2e.pages.category_page import CategoryPage
from test_data.test_category import TEST_CATEGORY_1
from test_data.test_product import TEST_PRODUCT_1
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.checkout_shipping_page import CheckoutShippingPage


@pytest.mark.e2e
@allure.title("Proceed to checkout (E2E)")
def test_e2e_proceed_to_checkout(config: dict, page: Page):
    print(f"{os.linesep}Running E2E test to proceed to checkout...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(config["username"], config["password"])

    category_page = CategoryPage(config, page, TEST_CATEGORY_1["seoPath"])
    category_page.navigate()

    product_card = category_page.get_product_card_by_sku(TEST_PRODUCT_1["sku"])
    product_card.quantity_input.fill("2")
    product_card.add_to_cart_text_button.click()

    cart_page = CartPage(config, page)
    cart_page.navigate()

    expect(cart_page.checkout_button).to_be_visible(), "Checkout button is not visible"
    expect(cart_page.checkout_button).to_be_enabled(), "Checkout button is not enabled"

    cart_page.checkout_button.click()

    checkout_page = CheckoutShippingPage(config, page)

    expect(checkout_page.page).to_have_url(checkout_page.url), "Checkout page is not loaded"

    cart_page.navigate()
    cart_page.clear_cart()
