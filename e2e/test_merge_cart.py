import pytest
from playwright.sync_api import Page
from e2e.pages.cart_page import CartPage
from e2e.pages.login_page import LoginPage


@pytest.fixture
def cart_page(page: Page, config):
    return CartPage(page, config)


@pytest.fixture
def login_page(page: Page, config):
    return LoginPage(page, config)


@pytest.fixture(autouse=True)
def cleanup(cart_page: CartPage):
    """Cleanup after each test"""
    yield  # This runs the test
    # After test cleanup
    cart_page.navigate()
    cart_page.clear_cart()
    cart_page.expect_cart_empty()


def test_merge_cart_anonymous_to_logged_in(cart_page: CartPage, login_page: LoginPage, config):
    """Test merging anonymous cart with logged-in user's cart
    
    Steps:
    1. Add product to cart as anonymous user
    2. Go to cart page
    3. Verify cart count and line item total
    4. Login as user
    5. Verify cart contents persist
    """
    # Preconditions
    product_url = "printers/multifunction-printers/laser-color/epson-workforce-wf-3640-all-in-one-printer"  # Replace with actual product name
    product_name = "ZZZitem for theme performance. Don't delete! Printer Epson"
    quantity = 2
    price = 60.00 # Replace with actual product price

    # Step 1: Add product to cart as anonymous user
    cart_page.add_product_to_cart(product_url, quantity)
    
    # Step 2: Go to cart page
    cart_page.click_cart_icon()
    
    # Step 3: Verify cart count and line item total    
    cart_page.expect_product_in_cart(product_name)
    cart_page.expect_line_item_total(price, quantity)
    
    # Step 4: Login as user
    login_page.navigate()
    login_page.login(config["username"], config["password"])
    login_page.expect_successful_login()
    
    # Step 5: Verify cart contents persist
    cart_page.click_cart_icon()   
    cart_page.expect_product_in_cart(product_name)
    cart_page.expect_line_item_total(price, quantity) 

