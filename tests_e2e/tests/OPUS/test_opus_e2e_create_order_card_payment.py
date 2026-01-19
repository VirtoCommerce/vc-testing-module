import os

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.requests_tracker import RequestsTracker
from test_data.test_category import TEST_CATEGORY_1
from test_data.test_product import TEST_PRODUCT_2
from test_data.test_supplier import TEST_SUPPLIER
from tests_e2e.pages.cart_page import CartPage
from tests_e2e.pages.category_page import CategoryPage
from tests_e2e.pages.checkout_billing_page import CheckoutBillingPage
from tests_e2e.pages.checkout_completed_page import CheckoutCompletedPage
from tests_e2e.pages.checkout_review_order_page import CheckoutReviewOrderPage
from tests_e2e.pages.checkout_shipping_page import CheckoutShippingPage
from tests_e2e.pages.sign_in_page import SignInPage
from tests_e2e.components.suppliers_filter_component import SuppliersFilterComponent
from fixtures.requests_tracker import RequestsTracker
from tests_e2e.components.quantity_stepper_component import QuantityStepperComponent
from tests_e2e.components.product_card_component import ProductCardComponent
from tests_e2e.pages.payment_form_page import PaymentFormPage

@pytest.mark.e2e
@allure.title("Create order with card payment (E2E)")
def test_e2e_create_order_with_card_payment(config: dict, page: Page, requests_tracker: RequestsTracker):
    print(f"{os.linesep}Running E2E test to create order with card payment...", end=" ")

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.sign_in(config["username"], config["password"])

    expect(page).not_to_have_url(sign_in_page.url), "Sign in page is still visible"

    category_page = CategoryPage(config, page, TEST_CATEGORY_1["seoPath"])
    category_page.navigate()
    requests_tracker.wait_for_all_requests()
    suppliers_filter_component = SuppliersFilterComponent(page)
    suppliers_filter_checkbox = suppliers_filter_component.get_supplier_checkbox(TEST_SUPPLIER["name"])
    suppliers_filter_checkbox.click()
    requests_tracker.wait_for_all_requests()
    
    product_to_add_to_cart = TEST_PRODUCT_2
    product_card = category_page.get_product_card_by_sku(product_to_add_to_cart["sku"])
    assert product_card is not None, (
        f"Product with SKU '{product_to_add_to_cart['sku']}' not found on category page. "
        f"Available products: {[card.sku for card in category_page.product_cards]}"
    )
    quantity_stepper_component = ProductCardComponent(product_card.element).quantity_stepper_component
    quantity_stepper_component.increment_button.click()
    requests_tracker.wait_for_all_requests()

    cart_page = CartPage(config, page)
    cart_page.navigate()
    cart_page.checkout_button.click()

    checkout_shipping_page = CheckoutShippingPage(config, page)
    requests_tracker.wait_for_all_requests()

    expect(page).to_have_url(
        checkout_shipping_page.url
    ), "Checkout shipping page is not loaded"
    
    requests_tracker.wait_for_all_requests()
    checkout_shipping_page.billing_button.click()

    checkout_billing_page = CheckoutBillingPage(config, page, requests_tracker)

    expect(page).to_have_url(
        checkout_billing_page.url
    ), "Checkout billing page is not loaded"
    requests_tracker.wait_for_all_requests()

    # Select card payment method
    checkout_billing_page.select_card_payment_method()
    
    # Open billing address selector
    checkout_billing_page.click_select_billing_address_button()
    
    # Print available addresses (optional, for debugging)
    checkout_billing_page.print_available_billing_addresses()
    
    # Select first billing address (index 0)
    checkout_billing_page.select_billing_address_by_index(0)
    
    expect(
        checkout_billing_page.review_order_button
    ).to_be_visible(), "Review order button is not visible"
    expect(
        checkout_billing_page.review_order_button
    ).to_be_enabled(), "Review order button is disabled"

    checkout_billing_page.review_order_button.click()

    checkout_review_order_page = CheckoutReviewOrderPage(config, page)

    expect(page).to_have_url(
        checkout_review_order_page.url
    ), "Checkout review order page is not loaded"
    expect(
        checkout_review_order_page.place_order_button
    ).to_be_visible(), "Place order button is not visible"
    expect(
        checkout_review_order_page.place_order_button
    ).to_be_enabled(), "Place order button is disabled"
    
    checkout_review_order_page.place_order_button.click()
    
    # Wait for navigation to payment page
    page.wait_for_url("**/checkout/payment", timeout=60000)
    page.wait_for_load_state("domcontentloaded")
    
    import time
    time.sleep(5)  # Give iframes time to load dynamically

    payment_form_page = PaymentFormPage(page)
    payment_form_page.fill_payment_form()
    requests_tracker.wait_for_all_requests()
    payment_form_page.click_pay_now_button()
    requests_tracker.wait_for_all_requests()

    checkout_completed_page = CheckoutCompletedPage(config, page)

    expect(page).to_have_url(
        checkout_completed_page.url
    ), "Checkout completed page is not loaded"

