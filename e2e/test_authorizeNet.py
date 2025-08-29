import pytest
from playwright.sync_api import Page
from e2e.pages.cart_page import CartPage
from e2e.pages.checkout_page import CheckoutPage
from e2e.pages.payment_page import PaymentPage
from e2e.pages.login_page import LoginPage
from e2e.pages.testData.test_data import (
    SHIPPING_DATA,
    PRODUCT,
    DELIVERY_METHOD1,
    DELIVERY_METHOD2,
    PAYMENT_METHOD1,
    PAYMENT_DATA,
    PAYMENT_DATA_FAILED,
)


@pytest.fixture
def cart_page(page: Page, config, browser_context):
    return CartPage(page, config, browser_context)


@pytest.fixture
def checkout_page(page: Page, config, browser_context):
    return CheckoutPage(page, config, browser_context)


@pytest.fixture
def payment_page(page: Page, config, browser_context):
    return PaymentPage(page, config, browser_context)


@pytest.fixture
def login_page(page: Page, config, browser_context):
    return LoginPage(page, config, browser_context)

@pytest.mark.skip(reason="Skipping test_payment_success")
def test_payment_success(
    cart_page: CartPage, checkout_page: CheckoutPage, payment_page: PaymentPage, login_page: LoginPage, config
):
    """Payment > Payment Success. Payment method is set to Authorize.Net"""
    # Setup test data

    product_url = PRODUCT["url"]
    product_name = PRODUCT["name"]
    quantity = PRODUCT["initial_quantity"]

    # Step 1: Add product to cart as user
    login_page.navigate()
    login_page.login(config["front_admin"], config["password_front_admin"])
    login_page.expect_successful_login()
    cart_page.click_cart_icon()
    cart_page.clear_cart()
    cart_page.expect_cart_empty()

    # Step 2: Add product to cart
    cart_page.add_product_to_cart(product_url, quantity)

    # Step 3: Go to cart page
    cart_page.click_cart_icon()

    # Step 4: Verify cart count and line item total
    cart_page.expect_product_in_cart(product_name, 1)
    cart_page.proceed_to_checkout()

    # Checkout steps
    checkout_page.select_delivery_method(DELIVERY_METHOD1)
    checkout_page.click_on_shipping_address(SHIPPING_DATA)
    checkout_page.check_shipping_page(DELIVERY_METHOD1, SHIPPING_DATA)
    checkout_page.proceed_to_billing()
    checkout_page.select_payment_method(PAYMENT_METHOD1)
    checkout_page.proceed_to_review()
    checkout_page.place_order()
    payment_page.check_payment_page(PAYMENT_METHOD1)
    payment_page.fill_payment_details(PAYMENT_DATA)
    payment_page.check_payment_success()

    # Step 5: Logout
    login_page.logout()
    print("Authorize.Net test payment success completed")


@pytest.mark.skip(reason="Skipping test_payment_failed")
def test_payment_failed(
    cart_page: CartPage, checkout_page: CheckoutPage, payment_page: PaymentPage, login_page: LoginPage, config
):
    """Payment > Payment Failed. Payment method is set to Authorize.Net"""
    # Setup test data

    product_url = PRODUCT["url"]
    product_name = PRODUCT["name"]
    quantity = PRODUCT["initial_quantity"]

    # Step 1: Add product to cart as user
    login_page.navigate()
    login_page.login(config["front_admin"], config["password_front_admin"])
    login_page.expect_successful_login()
    cart_page.click_cart_icon()
    cart_page.clear_cart()
    cart_page.expect_cart_empty()

    # Step 2: Add product to cart
    cart_page.add_product_to_cart(product_url, quantity)
    # Step 3: Go to cart page
    cart_page.click_cart_icon()
    # Step 4: Verify cart count and line item total
    cart_page.expect_product_in_cart(product_name, 1)
    cart_page.proceed_to_checkout()

    # Checkout steps
    checkout_page.select_delivery_method(DELIVERY_METHOD2)
    checkout_page.click_on_shipping_address(SHIPPING_DATA)
    checkout_page.check_shipping_page(DELIVERY_METHOD2, SHIPPING_DATA)
    checkout_page.proceed_to_billing()
    checkout_page.select_payment_method(PAYMENT_METHOD1)
    checkout_page.proceed_to_review()
    checkout_page.place_order()
    payment_page.check_payment_page(PAYMENT_METHOD1)
    payment_page.fill_payment_details(PAYMENT_DATA_FAILED)
    payment_page.check_payment_failure()

    # Step 5: Logout
    login_page.logout()
    print("Authorize.Net test payment failed completed")


@pytest.mark.skip(reason="Skipping test_payment_form_validation")
def test_payment_form_validation(
    cart_page: CartPage, checkout_page: CheckoutPage, payment_page: PaymentPage, login_page: LoginPage, config
):
    """Test validation when some card fields are filled"""
    # Add product to cart
    product_url = PRODUCT["url"]
    product_name = PRODUCT["name"]
    quantity = PRODUCT["initial_quantity"]

    login_page.navigate()
    login_page.login(config["front_admin"], config["password_front_admin"])
    login_page.expect_successful_login()
    cart_page.click_cart_icon()
    cart_page.clear_cart()
    cart_page.expect_cart_empty()

    cart_page.add_product_to_cart(product_url, quantity)
    cart_page.click_cart_icon()
    cart_page.expect_product_in_cart(product_name, 1)
    cart_page.proceed_to_checkout()

    checkout_page.select_delivery_method(DELIVERY_METHOD1)
    checkout_page.click_on_shipping_address(SHIPPING_DATA)
    checkout_page.check_shipping_page(DELIVERY_METHOD1, SHIPPING_DATA)
    checkout_page.proceed_to_billing()
    checkout_page.select_payment_method(PAYMENT_METHOD1)
    checkout_page.proceed_to_review()
    checkout_page.place_order()

    # Verify validation payment form fields
    payment_page.check_payment_page(PAYMENT_METHOD1)
    payment_page.validate_card_number_field()
    payment_page.clear_field("cvc")
    payment_page.clear_field("expiry")
    payment_page.clear_field("card_holder_name")
    payment_page.clear_field("card_number")

    payment_page.validate_card_holder_name_field()
    payment_page.clear_field("cvc")
    payment_page.clear_field("expiry")
    payment_page.clear_field("card_holder_name")
    payment_page.clear_field("card_number")

    payment_page.validate_expiry_field()
    payment_page.clear_field("cvc")
    payment_page.clear_field("expiry")
    payment_page.clear_field("card_holder_name")
    payment_page.clear_field("card_number")

    payment_page.validate_cvc_field()
    payment_page.clear_field("cvc")
    payment_page.clear_field("expiry")
    payment_page.clear_field("card_holder_name")
    payment_page.clear_field("card_number")

    print("Authorize.Net test form validation completed")
