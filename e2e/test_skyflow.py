import pytest
from playwright.sync_api import Page
from e2e.pages.cart_page import CartPage
from e2e.pages.checkout_page import CheckoutPage
from e2e.pages.payment_page import PaymentPage
from e2e.pages.login_page import LoginPage
from e2e.pages.saved_credit_cards_page import SavedCreditCardsPage
from e2e.pages.profile_page import ProfilePage
from e2e.pages.testData.test_data import SHIPPING_DATA, PRODUCT, DELIVERY_METHOD1, DELIVERY_METHOD2, PAYMENT_METHOD3, PAYMENT_SKYFLOW, PAYMENT_DATA_FAILED


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

@pytest.fixture
def saved_credit_cards_page(page: Page, config, browser_context):
    return SavedCreditCardsPage(page, config, browser_context)

@pytest.fixture
def profile_page(page: Page, config, browser_context):
    return ProfilePage(page, config, browser_context)

@pytest.fixture(autouse=True)
def cleanup():
    yield
    # Cleanup code


def test_payment_success(cart_page: CartPage, checkout_page: CheckoutPage, payment_page: PaymentPage, login_page: LoginPage, saved_credit_cards_page: SavedCreditCardsPage, profile_page: ProfilePage, config):
    """Payment > Bank card (Skyflow) > Save card checkbox is unchecked"""
    # Setup test data 
   
    product_url = PRODUCT["url"]
    product_name = PRODUCT["name"]
    quantity = PRODUCT["initial_quantity"] 
    payment_info = {
        "card_number": PAYMENT_SKYFLOW["visa_card_number"],
        "card_holder_name": PAYMENT_SKYFLOW["card_holder_name"],
        "expiry": PAYMENT_SKYFLOW["expiry"],
        "cvc": PAYMENT_SKYFLOW["cvc"]
    } 

    # Step 1: Add product to cart as user
    login_page.navigate()
    login_page.login(config["username"], config["password"])
    login_page.expect_successful_login()
    cart_page.click_cart_icon()
    cart_page.clear_cart()
    cart_page.expect_cart_empty()  

    # Go to saved credit cards page
    profile_page.click_dashboard()
    saved_credit_cards_page.click_saved_credit_cards_link()
    saved_credit_cards_page.delete_all_credit_cards()

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
    checkout_page.select_payment_method(PAYMENT_METHOD3)
    checkout_page.proceed_to_review()
    checkout_page.place_order()

    # Payment page
    payment_page.check_payment_page(PAYMENT_METHOD3)  
    payment_page.skyflow_new_form_fill(payment_info)
    payment_page.click_pay_now_button()
    payment_page.check_payment_success()
    
    # Go to saved credit cards page
    saved_credit_cards_page.navigate()
    saved_credit_cards_page.check_empty_view()

    # Step 5: Logout
    login_page.logout()
    print("Skyflow test payment success completed")



def test_payment_success_with_saved_card(cart_page: CartPage, checkout_page: CheckoutPage, payment_page: PaymentPage, login_page: LoginPage, saved_credit_cards_page: SavedCreditCardsPage, profile_page: ProfilePage, config):
    """Payment > Bank card (Skyflow) > Save a new Сard first time"""
    # Setup test data 
   
    product_url = PRODUCT["url"]
    product_name = PRODUCT["name"]
    quantity = PRODUCT["initial_quantity"]
    payment_info = {
        "card_number": PAYMENT_SKYFLOW["visa_card_number"],
        "card_holder_name": PAYMENT_SKYFLOW["card_holder_name"],
        "expiry": PAYMENT_SKYFLOW["expiry"],
        "cvc": PAYMENT_SKYFLOW["cvc"]
    } 

    # Step 1: Add product to cart as user
    login_page.navigate()
    login_page.login(config["username"], config["password"])
    login_page.expect_successful_login()
    cart_page.click_cart_icon()
    cart_page.clear_cart()
    cart_page.expect_cart_empty()  

    # Go to saved credit cards page
    profile_page.click_dashboard()
    saved_credit_cards_page.click_saved_credit_cards_link()
    saved_credit_cards_page.delete_all_credit_cards()

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
    checkout_page.select_payment_method(PAYMENT_METHOD3)
    checkout_page.proceed_to_review()
    checkout_page.place_order()

    # Payment page
    payment_page.check_payment_page(PAYMENT_METHOD3)
    payment_page.skyflow_new_form_fill(payment_info)
    payment_page.save_card_checkbox()
    payment_page.click_pay_now_button()
    payment_page.check_payment_success()

    # Go to saved credit cards page
    saved_credit_cards_page.navigate()
    saved_credit_cards_page.check_saved_credit_cards()

    # Step 5: Logout
    login_page.logout()
    print("Skyflow test payment success with saved card completed")

def test_payment_failed(cart_page: CartPage, checkout_page: CheckoutPage, payment_page: PaymentPage, login_page: LoginPage, saved_credit_cards_page: SavedCreditCardsPage, profile_page: ProfilePage, config):
    """Payment > Payment Failed. Payment method is set to Skyflow"""
    # Setup test data 
   
    product_url = PRODUCT["url"]
    product_name = PRODUCT["name"]
    quantity = PRODUCT["initial_quantity"] 
    payment_info = {
        "card_number": PAYMENT_SKYFLOW["master_card_number"],
        "card_holder_name": PAYMENT_SKYFLOW["card_holder_name"],
        "expiry": PAYMENT_DATA_FAILED["expiry"],
        "cvc": PAYMENT_DATA_FAILED["cvc"]
    } 

    # Step 1: Add product to cart as user
    login_page.navigate()
    login_page.login(config["username"], config["password"])
    login_page.expect_successful_login()
    cart_page.click_cart_icon()
    cart_page.clear_cart()
    cart_page.expect_cart_empty() 

    # Go to saved credit cards page
    profile_page.click_dashboard()
    saved_credit_cards_page.click_saved_credit_cards_link()
    saved_credit_cards_page.delete_all_credit_cards()

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
    checkout_page.select_payment_method(PAYMENT_METHOD3)
    checkout_page.proceed_to_review()
    checkout_page.place_order()
    payment_page.check_payment_page(PAYMENT_METHOD3)
    payment_page.skyflow_new_form_fill(payment_info)
    payment_page.click_pay_now_button()
    payment_page.check_payment_failure()

    # Go to saved credit cards page
    saved_credit_cards_page.navigate()
    saved_credit_cards_page.check_empty_view()

    # Step 5: Logout
    login_page.logout()
    print("Skyflow test payment failed completed")

@pytest.mark.skip(reason="Skipping test as it is not required")
def test_payment_form_validation(cart_page: CartPage, checkout_page: CheckoutPage, payment_page: PaymentPage, login_page: LoginPage, config):
    """Test validation when some card fields are filled"""
    # Add product to cart
    product_url = PRODUCT["url"]
    product_name = PRODUCT["name"]
    quantity = PRODUCT["initial_quantity"] 

   
    login_page.navigate()
    login_page.login(config["username"], config["password"])
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
    checkout_page.select_payment_method(PAYMENT_METHOD3)
    checkout_page.proceed_to_review()
    checkout_page.place_order()    
    
    # Verify validation payment form fields
    payment_page.check_payment_page(PAYMENT_METHOD3)   
    payment_page.validate_card_number_field()   
    clear_all_fields(payment_page)

    payment_page.validate_card_holder_name_field()
    clear_all_fields(payment_page)
 

    payment_page.validate_expiry_field()
    clear_all_fields(payment_page)
  

    payment_page.validate_cvc_field()
    clear_all_fields(payment_page)
   

    payment_page.validate_cvc_field()
    clear_all_fields(payment_page)
 
        
    print("Skyflow test form validation completed")

def clear_all_fields(self):
    fields = ["cvc", "expiry", "card_holder_name", "card_number"]
    for field in fields:
        self.clear_field(field)




