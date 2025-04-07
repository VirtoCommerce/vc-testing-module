from playwright.sync_api import Page, expect
from e2e.pages.locators.checkout_locators import CheckoutLocators
from utils.dialog_modal_actions import DialogModalActions


class CheckoutPage:
    def __init__(self, page: Page, config: dict):
        self.page = page
        self.config = config
        self.locators = CheckoutLocators
        self.dialog_modal_actions = DialogModalActions(self.page)

    def select_delivery_method(self, delivery_method: str):
        """Select delivery method"""
        self.page.click(self.locators.DELIVERY_METHOD_BUTTON)
        self.page.click(self.locators.DELIVERY_METHOD_FIXED_RATE.format(delivery_method))

    
    def click_on_shipping_address(self):
        """Click shipping address"""
        self.page.get_by_text(text="select a shipping address").is_visible()
        self.page.click(self.locators.SHIPING_ADDRESS_BUTTON)

    


    def fill_shipping_address(self, data: dict):
        """Fill shipping address form"""
        
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

    
    def check_shipping_page(self, delivery_method: str, data: dict):
        """Verify shipping page elements and delivery method"""
        # Check if delivery method is visible using the flex container selector
        expect(self.page.locator("div.flex.items-center.gap-3.p-\\[0\\.688rem\\].text-sm")).to_be_visible()
        expect(self.page.get_by_role("button", name=f"Fixed Rate ({delivery_method})")).to_be_visible()   
        expect(self.page.get_by_text(text=f"{data['address']}, {data['city']}, {data['country']}, {data['postcode']}")).to_be_visible()        
 

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
                expect(self.page.locator(self.locators.PAYMENT_METHOD_CREDIT_CARD)).to_be_visible()
                self.page.click(self.locators.PAYMENT_METHOD_CREDIT_CARD)
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
            self.page.fill(self.locators.BILLING_FIRST_NAME, billing_info["first_name"])
            self.page.fill(self.locators.BILLING_LAST_NAME, billing_info["last_name"])
            self.page.fill(self.locators.BILLING_EMAIL, billing_info["email"])
            self.page.fill(self.locators.BILLING_PHONE, billing_info["phone"])
            self.page.fill(self.locators.BILLING_ADDRESS_1, billing_info["address"])
            self.page.fill(self.locators.BILLING_CITY, billing_info["city"])
            
            # Wait for form to be filled
            self.page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Error in fill_billing_details: {str(e)}")
            raise

    def enter_payment_details(self, payment_info: dict):
        """Enter payment information"""
        self.page.fill(self.locators.CARD_NUMBER, payment_info["card_number"])
        self.page.fill(self.locators.CARD_EXPIRY, payment_info["expiry"])
        self.page.fill(self.locators.CARD_CVC, payment_info["cvc"])