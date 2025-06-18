import pytest
from playwright.sync_api import Page
from e2e.pages.cart_page import CartPage
from e2e.pages.checkout_page import CheckoutPage
from e2e.pages.testData.test_data import (
    SHIPPING_DATA,
    PRODUCT,
    DELIVERY_METHOD1,
    DELIVERY_METHOD2,
    PAYMENT_METHOD1,
    PAYMENT_METHOD4,
)


@pytest.fixture
def cart_page(page: Page, config, browser_context):
    return CartPage(page, config, browser_context)


@pytest.fixture
def checkout_page(page: Page, config, browser_context):
    return CheckoutPage(page, config, browser_context)


def test_anonymous_complete_checkout(cart_page: CartPage, checkout_page: CheckoutPage):
    """Test complete checkout flow"""
    # Setup test data

    product_url = PRODUCT["url"]
    product_name = PRODUCT["name"]
    quantity = PRODUCT["initial_quantity"]
    change_quantity = PRODUCT["updated_quantity"]
    price = PRODUCT["price"]

    # Step 1: Add product to cart as anonymous user
    cart_page.add_product_to_cart(product_url, quantity)

    # Step 2: Go to cart page
    cart_page.click_cart_icon()

    # Step 3: Verify cart count and line item total
    cart_page.expect_product_in_cart(product_name, 1)
    cart_page.expect_line_item_total(product_name, price, quantity, 1, 3)
    cart_page.expect_subtotal(price * quantity)

    # Set valid quantity and verify subtotal
    cart_page.set_quantity(change_quantity)
    cart_page.expect_line_item_total(product_name, price, change_quantity, 1, 3)
    cart_page.expect_subtotal(price * change_quantity)
    cart_page.proceed_to_checkout()

    # Checkout steps
    checkout_page.select_delivery_method(DELIVERY_METHOD1)
    checkout_page.click_on_shipping_address(SHIPPING_DATA)
    checkout_page.check_shipping_page(DELIVERY_METHOD1, SHIPPING_DATA)
    checkout_page.proceed_to_billing()
    checkout_page.select_payment_method(PAYMENT_METHOD4)
    checkout_page.proceed_to_review()
    checkout_page.place_order()
    checkout_page.expect_completed_order()
