from playwright.sync_api import Page, expect, BrowserContext
from e2e.pages.locators.checkout_locators import CheckoutLocators
from e2e.pages.locators.cart_locators import CartLocators
from utils.dialog_modal_actions import DialogModalActions
from utils.commonLocators.common_components_locators import CommonComponentsLocators

class CheckoutPage:
    def __init__(self, page: Page, config: dict, browser_context: BrowserContext):
        self.page = page
        self.config = config
        self.browser_context = browser_context
        self.locators = CheckoutLocators
        self.dialog_modal_actions = DialogModalActions(self.page)

    def select_delivery_method(self, delivery_method: str):
        """Select delivery method"""
        self.page.click(self.locators.DELIVERY_METHOD_BUTTON)
        self.page.click(self.locators.DELIVERY_METHOD_FIXED_RATE.format(delivery_method))

    
    def click_on_shipping_address(self, data: dict = None):
        """Click shipping address"""
        self.page.get_by_text(text="select a shipping address").is_visible()
        self.page.click(self.locators.SHIPING_ADDRESS_BUTTON)
        self.dialog_modal_actions.check_dialog_modal_is_open()
        if self.dialog_modal_actions.check_dialog_modal_title("New address"):
            self.fill_shipping_address(data)              
        else:
            self.dialog_modal_actions.check_dialog_modal_title("Select address")
            self.select_shiping_address()

    


    def fill_shipping_address(self, data: dict = None):
        """Fill shipping address form"""
        if data is None:
            # Use default test data if none provided
            data = {
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "phone": "1234567890",
                "address": "123 Test St",
                "city": "Test City",
                "zip_code": "12345",
                "country": "United States"
            }
        
        self.page.fill(self.locators.FIRST_NAME, data["first_name"])
        self.page.fill(self.locators.LAST_NAME, data["last_name"])
        self.page.fill(self.locators.EMAIL, data["email"]) 
        self.page.fill(self.locators.PHONE, data["phone"])
        self.page.get_by_placeholder("Select your country").click()
        self.page.get_by_text(data["country"]).click()
        self.page.fill(self.locators.ADDRESS_1, data["address"])        
        self.page.fill(self.locators.CITY, data["city"])        
        self.page.fill(self.locators.POSTCODE, data["postcode"])
        self.dialog_modal_actions.check_create_button()
        self.dialog_modal_actions.click_create_button()
        self.dialog_modal_actions.check_dialog_modal_is_closed()


    def select_shiping_address(self):
        """Select shipping address"""
        self.page.click(CheckoutLocators.SELECT_SHIPING_ADDRESS)
        self.dialog_modal_actions.click_dialog_modal_button_OK()
       

    
    def check_shipping_page(self, delivery_method: str, data: dict):
        """Verify shipping page elements and delivery method"""
        # Check if delivery method is visible using the flex container selector
        expect(self.page.locator("div.flex.items-center.gap-3.p-\\[0\\.688rem\\].text-sm")).to_be_visible()
        expect(self.page.get_by_role("button", name=f"Fixed Rate ({delivery_method})")).to_be_visible()   
        expect(self.page.locator(CheckoutLocators.SELECTED_SHIPPING_ADDRESS)).to_be_visible()        
 

    def proceed_to_billing(self):
        """Proceed to billing"""
        try:
            # Wait for the button to be visible and enabled
            self.page.wait_for_load_state("networkidle")            
            expect(self.page.get_by_text("Proceed to billing")).to_be_visible()
            expect(self.page.get_by_text("Proceed to billing")).to_be_enabled()
            
            # Click with retry mechanism            
            self.page.get_by_text("Proceed to billing").click()           
            self.page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Error in proceed_to_billing: {str(e)}")
            raise

    def select_payment_method(self, method: str):
        """Select payment method"""
        try:
            # Wait for payment method button to be visible
            expect(self.page.locator(self.locators.PAYMENT_METHOD_BUTTON)).to_be_visible()
            self.page.click(self.locators.PAYMENT_METHOD_BUTTON)
            
            # Wait for payment options to be visible
            self.page.wait_for_load_state("networkidle")
            
            if method == "Authorize.Net" or method == "CyberSource" or method == "Skyflow":
                expect(self.page.locator(self.locators.PAYMENT_METHOD_CREDIT_CARD.format(method))).to_be_visible()
                self.page.click(self.locators.PAYMENT_METHOD_CREDIT_CARD.format(method))
            elif method == "Manual":
                expect(self.page.locator(self.locators.PAYMENT_METHOD_MANUAL.format(method))).to_be_visible()
                self.page.click(self.locators.PAYMENT_METHOD_MANUAL.format(method))
            else:
                expect(self.page.get_by_text(method)).to_be_visible()
                self.page.get_by_text(method).click()
                
            # Wait for selection to be applied
            self.page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Error in select_payment_method: {str(e)}")
            raise

    def proceed_to_review(self):
        """Proceed to review"""
        try:
            # Wait for the button to be visible and enabled          
            expect(self.page.get_by_text("Review order")).to_be_visible()
            expect(self.page.get_by_text("Review order")).to_be_enabled()
            
            # Click with retry mechanism
            self.page.get_by_text("Review order").click()
            
            # Wait for navigation to complete
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")
        except Exception as e:
            print(f"Error in proceed_to_review: {str(e)}")
            raise

    def place_order(self):
        """Place order"""
        try:
            # Wait for the button to be visible and enabled          
            expect(self.page.get_by_text("Place order")).to_be_visible()
            expect(self.page.get_by_text("Place order")).to_be_enabled()
            
            # Click with retry mechanism
            self.page.get_by_text("Place order").click()
            self.page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Error in place_order: {str(e)}")
            raise


    def expect_completed_order(self):
        """Verify order completion"""
        expect(self.page).to_have_url(f"{self.config['base_url']}/checkout/completed")

    def fill_billing_details(self, billing_info: dict):
        """Fill billing information"""
        try:
            # Wait for billing form to be visible
            self.page.wait_for_load_state("networkidle")
            
            # Fill in billing details
            self.page.fill(self.locators.FIRST_NAME, billing_info["first_name"])
            self.page.fill(self.locators.LAST_NAME, billing_info["last_name"])
            self.page.fill(self.locators.EMAIL, billing_info["email"])
            self.page.fill(self.locators.PHONE, billing_info["phone"])
            self.page.fill(self.locators.ADDRESS_1, billing_info["address"])
            self.page.fill(self.locators.CITY, billing_info["city"])
            
            # Wait for form to be filled
            self.page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Error in fill_billing_details: {str(e)}")
            raise 
        
    def expect_order_review_items_count(self, expected_count: int):
        """Verify the number of items in the order review page"""
        # Use first() to select the first matching element
        self.page.locator(CheckoutLocators.ORDER_REVIEW_ITEMS).first.wait_for(state="visible")
        order_items = self.page.locator(CartLocators.LINE_ITEM).count()
        assert order_items == expected_count, f"Expected {expected_count} items in order review, but found {order_items}"
        print(f"Review order items: {order_items}")
    
    def check_order_review_page(self):
        """Check order review page"""        
        expect(self.page.get_by_text("Please review your order")).to_be_visible()
        order_line_items = self.page.locator(CheckoutLocators.ORDER_REVIEW_ITEMS).count()
        print(f"Vendor order line items: {order_line_items}")
        if order_line_items > 1:
            items = self.page.locator(CheckoutLocators.ORDER_REVIEW_ITEMS).all()
            for item in items:
                expect(item).to_be_visible()        
           
        else:
            expect(self.page.locator(CheckoutLocators.ORDER_REVIEW_ITEMS)).to_be_visible()
        expect(self.page.locator(CheckoutLocators.ORDER_REVIEW_WIDGET)).to_be_visible() 


        
        
