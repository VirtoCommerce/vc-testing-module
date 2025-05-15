import pytest
from playwright.sync_api import Page, expect
from e2e.pages.cart_page import CartPage
from e2e.pages.checkout_page import CheckoutPage
from e2e.pages.catalog_page import CatalogPage
from e2e.pages.testData.test_data import SHIPPING_DATA, DELIVERY_METHOD1, PAYMENT_METHOD1, PAYMENT_DATA
from e2e.pages.testData.search_data import random_search_data
from e2e.pages.login_page import LoginPage
from e2e.pages.payment_page import PaymentPage
from e2e.pages.search_page import SearchPage


@pytest.fixture
def cart_page(page: Page, config, browser_context):
    return CartPage(page, config, browser_context)

@pytest.fixture
def checkout_page(page: Page, config, browser_context):
    return CheckoutPage(page, config, browser_context)

@pytest.fixture
def catalog_page(page: Page, config, browser_context):
    return CatalogPage(page, config, browser_context)

@pytest.fixture
def login_page(page: Page, config):
    return LoginPage(page, config)

@pytest.fixture
def payment_page(page: Page, config, browser_context):
    return PaymentPage(page, config, browser_context)

@pytest.fixture
def search_page(page: Page, config, browser_context):
    return SearchPage(page, config, browser_context)

@pytest.fixture(autouse=True)
def login_logout(login_page: LoginPage, cart_page: CartPage, config):
    """Login and logout for each test"""
    login_page.navigate()
    login_page.login(config["username"], config["password"])
    cart_page.navigate()
    cart_page.clear_cart()   
    cart_page.expect_cart_empty()
    yield
    cart_page.navigate()
    cart_page.clear_cart()   
    cart_page.expect_cart_empty()
    login_page.logout()


def test_select_unselect_items(cart_page: CartPage, checkout_page: CheckoutPage, catalog_page: CatalogPage, payment_page: PaymentPage, search_page: SearchPage):
    """Test case C389845: add 4 items > unselect all > select 2 > create an order"""
    # Setup test data
    total_items = 4
    selected_items = 2
    search_data = random_search_data()   

    print("Adding products to the cart")
    print(f"Search data: {search_data}")    
    search_page.verify_search_results(search_data)
    catalog_page.add_items_to_cart_one_by_one(total_items)
    
    cart_page.click_cart_icon()      
    cart_page.get_line_items()  
    
    print("Verifying all products are selected by default")
    cart_page.expect_product_count(total_items)
    cart_page.expect_all_items_selected()
    
    print("Unselecting all items")
    cart_page.unselect_all_items()
    cart_page.page.wait_for_load_state("networkidle")
    cart_page.page.wait_for_selector('.vc-loader-overlay__spinner', state="hidden")
    cart_page.expect_all_items_unselected()
    cart_page.check_subtotal(0.000)    
    cart_page.expect_proceed_to_checkout_disabled()
    
    print(f"Selecting only: {selected_items} of {total_items}")    
    cart_page.select_items(selected_items) 
    cart_page.expect_selected_items_count(selected_items)        
    cart_page.expect_proceed_to_checkout_enabled()   
    
    cart_page.proceed_to_checkout()   

    checkout_page.select_delivery_method(DELIVERY_METHOD1)
    checkout_page.click_on_shipping_address()    
    checkout_page.check_shipping_page(DELIVERY_METHOD1, SHIPPING_DATA)
    checkout_page.proceed_to_billing()    
    
    checkout_page.select_payment_method(PAYMENT_METHOD1)
    checkout_page.proceed_to_review()
    checkout_page.check_order_review_page()    
    checkout_page.expect_order_review_items_count(selected_items)
    
    checkout_page.place_order()
    payment_page.check_payment_page(PAYMENT_METHOD1)
    payment_page.fill_payment_details(PAYMENT_DATA)
    payment_page.check_payment_success()
    
    print("Go to cart and check remaining items")
    cart_page.navigate()
    cart_page.expect_product_count(total_items - selected_items)
    cart_page.expect_all_items_selected()