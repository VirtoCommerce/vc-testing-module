import pytest
from playwright.sync_api import Page
from e2e.pages.cart_page import CartPage
from e2e.pages.login_page import LoginPage
from utils.logout import LogoutPage


@pytest.fixture
def cart_page(page: Page, config, browser_context):
    return CartPage(page, config, browser_context)


@pytest.fixture
def login_page(page: Page, config, browser_context):
    return LoginPage(page, config, browser_context)


@pytest.fixture
def logout_page(page: Page, config, browser_context):
    return LogoutPage(page, config, browser_context)


@pytest.fixture(autouse=True)
def cleanup(cart_page: CartPage, request):
    """Cleanup after each test"""
    # Skip cleanup for test_merge_anonymous_user_cart
    if request.node.name == "test_merge_anonymous_user_cart":
        yield
        return
        
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
    cart_page.expect_product_in_cart(product_name, 1)
    cart_page.expect_line_item_total(product_name, price, quantity, 1, 3)
    
    # Step 4: Login as user
    login_page.navigate()
    login_page.login(config["username"], config["password"])
    login_page.expect_successful_login()
    
    # Step 5: Verify cart contents persist
    cart_page.click_cart_icon()   
    cart_page.expect_product_in_cart(product_name, 1)
    cart_page.expect_line_item_total(product_name, price, quantity, 1, 3)


def test_merge_anonymous_user_cart(cart_page: CartPage, login_page: LoginPage, logout_page: LogoutPage, config):
    """Test merging anonymous cart with user cart   
    
    Steps:
    1. Login as user
    2. Add product to cart
    3. Logout
    4. Add product to cart as anonymous user
    5. Login as user
    6. Verify merged cart contains all products
    """
    # Test data
    user_product = "HP Color LaserJet Enterprise Flow MFP M577z Wireless Printer, Copy/Fax/Print/Scan"
    user_url = "printers/multifunction-printers/laser-color/hp-color-laserjet-enterprise-flow-mfp-m577z-wireless-printer-copyfaxprintscan-color-black-white"
    user_quantity = 2
    user_price = 750.00
    
    anonymous_product = "ZZZitem for theme performance. Don't delete! Printer Epson"
    anonymous_url = "printers/multifunction-printers/laser-color/epson-workforce-wf-3640-all-in-one-printer"
    anonymous_quantity = 1
    anonymous_price = 60.00

    # Step 1: Login as user
    login_page.navigate()
    login_page.login(config["username"], config["password"])
    login_page.expect_successful_login()
    cart_page.click_cart_icon()
    cart_page.clear_cart()
    cart_page.expect_cart_empty()
    
    # Step 2: Add product to cart as user
    cart_page.add_product_to_cart(user_url, user_quantity)
    cart_page.click_cart_icon()
    cart_page.expect_cart_count(user_quantity, user_quantity)
    cart_page.expect_product_in_cart(user_product, 1)
    cart_page.expect_line_item_total(user_product, user_price, user_quantity, 1, 3)
    
    # Step 3: Logout
    logout_page.logout()
    logout_page.expect_logged_out()
    
    # Step 4: Add product to cart as anonymous user
    cart_page.add_product_to_cart(anonymous_url, anonymous_quantity)
    cart_page.click_cart_icon()
    cart_page.expect_cart_count(anonymous_quantity, anonymous_quantity)
    cart_page.expect_product_in_cart(anonymous_product, 1)
    cart_page.expect_line_item_total(anonymous_product, anonymous_price, anonymous_quantity, 1, 3)
    
    # Step 5: Login as user
    login_page.navigate()
    login_page.login(config["username"], config["password"])
    login_page.expect_successful_login()
    
    # Step 6: Verify merged cart
    cart_page.click_cart_icon()
    
    # Verify both products are present
    cart_page.expect_product_in_cart(user_product, 2)
    cart_page.expect_product_in_cart(anonymous_product, 1)             
    
    # Verify quantities and prices are correct for each product
    cart_page.expect_line_item_total(user_product, user_price, user_quantity, 2, 6)
    cart_page.expect_line_item_total(anonymous_product, anonymous_price, anonymous_quantity, 1, 3)
    
    # Verify total cart count
    total_quantity = user_quantity + anonymous_quantity
    cart_page.expect_cart_count(total_quantity, total_quantity)

