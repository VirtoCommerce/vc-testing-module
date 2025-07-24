import allure, os, pytest
from playwright.sync_api import Page, expect
from tests_e2e.pages.category_page import CategoryPage
from tests_e2e.pages.sign_in_page import SignInPage
from test_data.test_category import TEST_CATEGORY_1
from test_data.test_product import TEST_PRODUCT_1
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.checkout_shipping_page import CheckoutShippingPage
from tests_e2e.pages.checkout_billing_page import CheckoutBillingPage
from tests_e2e.pages.checkout_review_order_page import CheckoutReviewOrderPage
from tests_e2e.pages.checkout_completed_page import CheckoutCompletedPage
from fixtures.requests_tracker_fixture import RequestsTracker


@pytest.mark.e2e
@allure.title("Create order (E2E)")
def test_e2e_create_order(config: dict, page: Page, requests_tracker: RequestsTracker):
    print(f"{os.linesep}Running E2E test to create order...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(config["username"], config["password"])

    expect(page).not_to_have_url(sign_in_page.url), "Sign in page is still visible"

    category_page = CategoryPage(config, page, TEST_CATEGORY_1["seoPath"])
    category_page.navigate()

    product_card = category_page.get_product_card_by_sku(TEST_PRODUCT_1["sku"])
    product_card.quantity_input.fill("2")
    product_card.add_to_cart_text_button.click()

    cart_page = CartPage(config, page)
    cart_page.navigate()
    cart_page.checkout_button.click()

    checkout_shipping_page = CheckoutShippingPage(config, page)

    expect(page).to_have_url(checkout_shipping_page.url), "Checkout shipping page is not loaded"

    checkout_shipping_page.shipping_details_section_component.switch_delivery_option("shipping")

    expect(checkout_shipping_page.shipping_details_section_component.address_selector_component.element).to_be_visible(), "Shipping address section is not visible"
    expect(checkout_shipping_page.shipping_details_section_component.shipping_method_selector).to_be_visible(), "Shipping method selector is not visible"
    expect(checkout_shipping_page.shipping_details_section_component.address_selector_component.selected_address_label).to_be_visible(), "Selected address label is not visible"
    expect(checkout_shipping_page.shipping_details_section_component.address_selector_component.selected_address_label).not_to_be_empty(), "Selected address label is empty"

    checkout_shipping_page.shipping_details_section_component.select_shipping_method("FixedRate_Ground")

    requests_tracker.wait_for_all_requests()

    expect(checkout_shipping_page.billing_button).to_be_visible(), "Billing button is not visible"
    expect(checkout_shipping_page.billing_button).to_be_enabled(), "Billing button is disabled"

    checkout_shipping_page.billing_button.click()

    checkout_billing_page = CheckoutBillingPage(config, page)

    expect(page).to_have_url(checkout_billing_page.url), "Checkout billing page is not loaded"

    checkout_billing_page.select_payment_method("DefaultManualPaymentMethod")

    requests_tracker.wait_for_all_requests()

    expect(checkout_billing_page.review_order_button).to_be_visible(), "Review order button is not visible"
    expect(checkout_billing_page.review_order_button).to_be_enabled(), "Review order button is disabled"

    checkout_billing_page.review_order_button.click()

    checkout_review_order_page = CheckoutReviewOrderPage(config, page)

    expect(page).to_have_url(checkout_review_order_page.url), "Checkout review order page is not loaded"
    expect(checkout_review_order_page.place_order_button).to_be_visible(), "Place order button is not visible"
    expect(checkout_review_order_page.place_order_button).to_be_enabled(), "Place order button is disabled"

    checkout_review_order_page.place_order_button.click()

    checkout_completed_page = CheckoutCompletedPage(config, page)

    expect(page).to_have_url(checkout_completed_page.url), "Checkout completed page is not loaded"

    print(f"Order number: {checkout_completed_page.order_number}")
    assert checkout_completed_page.order_number is not None, "Order number is not found"
