import pytest
from playwright.sync_api import Page
from e2e.pages.cart_page import CartPage
from e2e.pages.checkout_page import CheckoutPage

@pytest.fixture
def cart_page(page: Page, config):
    return CartPage(page, config)

@pytest.fixture
def checkout_page(page: Page, config):
    return CheckoutPage(page, config)

def test_anonymous_complete_checkout(cart_page: CartPage, checkout_page: CheckoutPage):
    """Test complete checkout flow"""
    # Setup test data
    shipping_data = {
        "first_name": "AnnaTab",
        "last_name": "MTab",
        "email": "weiewfoiu@jhkrgh.rgw",
        "phone": "32423",
        "address": "efwe",
        "city": "fwefewg"
    }

    # Cart steps
        # Preconditions
    product_url = "printers/multifunction-printers/laser-color/epson-workforce-wf-3640-all-in-one-printer"  # Replace with actual product name
    product_name = "ZZZitem for theme performance. Don't delete! Printer Epson"
    quantity = 2
    change_quantity = 3
    price = 60.00 # Replace with actual product price

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
    checkout_page.select_delivery_method()
    checkout_page.fill_shipping_address(shipping_data)
    checkout_page.proceed_to_billing()
    checkout_page.select_payment_method()
    checkout_page.proceed_to_review()
    checkout_page.place_order()
    checkout_page.expect_completed_order() 