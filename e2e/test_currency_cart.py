import pytest
from playwright.sync_api import Page
from e2e.pages.cart_page import CartPage
from e2e.pages.login_page import LoginPage
from e2e.pages.profile_page import ProfilePage
from utils.logout import LogoutPage
from e2e.pages.testData.test_data import CURRENCY_TEST_PRODUCT
from e2e.pages.language_currency_selector import LanguageCurrencySelector

@pytest.fixture
def profile_page(page: Page, config) -> ProfilePage:   
    return ProfilePage(page, config)

@pytest.fixture
def cart_page(page: Page, config):
    return CartPage(page, config)

@pytest.fixture
def login_page(page: Page, config):
    return LoginPage(page, config)

@pytest.fixture
def logout_page(page: Page, config):
    return LogoutPage(page, config)

@pytest.fixture
def language_currency_selector(page: Page):
    return LanguageCurrencySelector(page)

def test_change_user_currency(cart_page: CartPage, login_page: LoginPage, config, profile_page: ProfilePage, logout_page: LogoutPage, language_currency_selector: LanguageCurrencySelector):
    """Test changing user's currency
    
    Steps:
    1. Login as user
    2. Add product to cart
    3. Change currency to EUR
    4. Verify profile updated
    5. Logout
    """
    # Step 1: Go to cart and click Sign in
    login_page.navigate()

    # Step 2: Login as user
    login_page.login(config["username"], config["password"])
    login_page.expect_successful_login()
    cart_page.click_cart_icon()
    cart_page.clear_cart()
    cart_page.expect_cart_empty()    

    # Step 3: Add first product to cart
    cart_page.add_product_to_cart(CURRENCY_TEST_PRODUCT["url"], CURRENCY_TEST_PRODUCT["quantity"])
    cart_page.click_cart_icon()    
    cart_page.expect_product_in_cart(CURRENCY_TEST_PRODUCT["name"], 1)  
    cart_page.expect_product_count(1)

    profile_page.click_dashboard()
    profile_page.click_profile()
    profile_page.change_currency("EUR")
    profile_page.update_profile()
    logout_page.logout()

def test_check_currency_in_cart(cart_page: CartPage, config, login_page: LoginPage, logout_page: LogoutPage, language_currency_selector: LanguageCurrencySelector):
    """Test checking currency in cart
    
    Steps:
    1. Login as user
    2. Verify currency is EUR
    3. Verify product in cart   
    4. Logout
    """
    # Step 1: Login as user
    login_page.navigate()
    login_page.login(config["username"], config["password"])
    login_page.expect_successful_login()
    cart_page.click_cart_icon()
    cart_page.expect_product_count(1)    
    cart_page.expect_product_in_cart(CURRENCY_TEST_PRODUCT["name"], 1)
    cart_page.extract_currency_symbol()
    language_currency_selector.expect_currency_change("EUR")
    logout_page.logout()  



def test_merge_cart_change_currency(cart_page: CartPage, config, login_page: LoginPage, language_currency_selector: LanguageCurrencySelector, profile_page: ProfilePage, logout_page: LogoutPage):
    """Test merging cart and changing currency
    
    Steps:
    1. Add product to usd cart as anonymous user
    2. Login as user
    3. Verify cart contents persist 
    4. Verify currency is EUR   
    
    """
    # Step 1: Add product to usd cart as anonymous user
    cart_page.add_product_to_cart(CURRENCY_TEST_PRODUCT["url_2"], CURRENCY_TEST_PRODUCT["quantity_2"])
    cart_page.click_cart_icon()  
    cart_page.expect_product_in_cart(CURRENCY_TEST_PRODUCT["name_2"], 1)
    cart_page.expect_line_item_total(CURRENCY_TEST_PRODUCT["name_2"], CURRENCY_TEST_PRODUCT["price_2"], CURRENCY_TEST_PRODUCT["quantity_2"], 1, 3)
    cart_page.expect_subtotal(CURRENCY_TEST_PRODUCT["price_2"] * CURRENCY_TEST_PRODUCT["quantity_2"])

    # Step 2: Login as user
    login_page.navigate()
    login_page.login(config["username"], config["password"])
    login_page.expect_successful_login()
    cart_page.click_cart_icon()    
    cart_page.expect_product_count(1)   
    cart_page.expect_product_in_cart(CURRENCY_TEST_PRODUCT["name_2"], 1)
    cart_page.extract_currency_symbol()    
    language_currency_selector.expect_currency_change("EUR")

    profile_page.click_dashboard()
    profile_page.click_profile()
    profile_page.change_currency("USD")
    profile_page.update_profile()
    logout_page.logout()

   
       






