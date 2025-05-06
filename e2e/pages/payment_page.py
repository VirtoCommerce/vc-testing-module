from e2e.pages.locators.checkout_locators import CheckoutLocators
from playwright.sync_api import Page, BrowserContext, expect
from utils.commonLocators.common_components_locators import CommonComponentsLocators

class PaymentPage:
    def __init__(self, page: Page, config: dict, browser_context: BrowserContext):
        self.page = page
        self.config = config
        self.browser_context = browser_context

    def check_payment_page(self, payment_method: str):
        """Check payment page"""
        expect(self.page).to_have_url(self.config["base_url"] + CheckoutLocators.PAYMENT_PAGE_URL)
        print(f"Payment page URL: {self.config['base_url'] + CheckoutLocators.PAYMENT_PAGE_URL}")
        self.page.locator(CheckoutLocators.PAYMENT_PAGE_TITLE).wait_for(state="visible")
        self.page.locator(CheckoutLocators.PAYMENT_METHOD.format(payment_method)).wait_for(state="visible")
        self.page.locator(CheckoutLocators.PAYMENT_FORM).wait_for(state="visible")
    
    def fill_payment_details(self, payment_info: dict):
        """Fill payment details"""
        self.page.locator(CheckoutLocators.CARD_NUMBER).fill(payment_info["card_number"])
        self.page.locator(CheckoutLocators.CARD_HOLDER_NAME).fill(payment_info["card_holder_name"])
        self.page.locator(CheckoutLocators.CARD_EXPIRY).fill(payment_info["expiry"])
        self.page.locator(CheckoutLocators.CARD_CVC).fill(payment_info["cvc"])
        expect(self.page.locator(CheckoutLocators.PAY_NOW_BUTTON)).to_be_visible()        
        self.page.locator(CheckoutLocators.PAY_NOW_BUTTON).click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")               
        

    def expect_validation_message(self, message: str):
        """Verify validation message for a specific field"""       
        validation_message = self.page.locator("//div[@class='vc-input-details__message']")        
        # Verify the validation message text
        expect(validation_message).to_have_text(message)

    def check_payment_success(self):
        """Check payment success"""      
        self.page.locator(CheckoutLocators.PAYMENT_SUCCESS).wait_for(state="visible")
        expect(self.page).to_have_url(self.config["base_url"] + CheckoutLocators.PAYMENT_SUCCESS_URL)
        expect(self.page.locator(CheckoutLocators.SHOW_ORDER_BUTTON)).to_be_visible()
        print(f"Expected result: payment success")


    def check_payment_failure(self):
        """Check payment failure"""
        self.page.wait_for_timeout(10000)
        self.page.locator(CheckoutLocators.PAYMENT_FAILURE).wait_for(state="visible")
        expect(self.page).to_have_url(self.config["base_url"] + CheckoutLocators.PAYMENT_FAILURE_URL)
        print(f"Expected result: payment failure")

    def validate_card_number_field(self):
        """Validate card number field is required"""
        self.page.locator(CheckoutLocators.CARD_NUMBER).fill("5252525252525252")
        self.clear_field("card_number")
        self.page.locator(CheckoutLocators.CARD_HOLDER_NAME).fill("John Doe")
        self.page.locator(CheckoutLocators.CARD_EXPIRY).fill("01/30")
        self.page.locator(CheckoutLocators.CARD_CVC).fill("900")
        # Click away from the field to trigger validation        
        self.expect_validation_message("This field is required")
        expect(self.page.locator(CheckoutLocators.PAY_NOW_BUTTON)).to_be_disabled() 

    def validate_card_holder_name_field(self):
        """Validate card holder name field is required"""
        self.page.locator(CheckoutLocators.CARD_NUMBER).fill("4111111111111111")
        self.page.locator(CheckoutLocators.CARD_HOLDER_NAME).fill("ryr")
        self.clear_field("card_holder_name")
        self.page.locator(CheckoutLocators.CARD_EXPIRY).fill("01/30")
        self.page.locator(CheckoutLocators.CARD_CVC).fill("123")
        # Click away from the field to trigger validation
        self.page.locator(CheckoutLocators.CARD_NUMBER).click()
        self.expect_validation_message("This field is required")
        expect(self.page.locator(CheckoutLocators.PAY_NOW_BUTTON)).to_be_disabled()        
        # Test with more than 64 characters
        self.clear_field("card_holder_name")
        long_name = "A" * 65  # Create a string with 65 characters
        self.page.locator(CheckoutLocators.CARD_HOLDER_NAME).fill(long_name)
        self.page.locator(CheckoutLocators.CARD_NUMBER).click()
        self.expect_validation_message("This field must not contain more than 64 characters")
        expect(self.page.locator(CheckoutLocators.PAY_NOW_BUTTON)).to_be_disabled()

    def validate_expiry_field(self):
        """Validate expiry field is required"""
        self.page.locator(CheckoutLocators.CARD_NUMBER).fill("4111111111111111")
        self.page.locator(CheckoutLocators.CARD_HOLDER_NAME).fill("John Doe")
        self.page.locator(CheckoutLocators.CARD_EXPIRY).fill("")
        self.page.locator(CheckoutLocators.CARD_CVC).fill("123")
        # Click away from the field to trigger validation
        self.page.locator(CheckoutLocators.CARD_HOLDER_NAME).click()
        self.expect_validation_message("This field is required")       
        expect(self.page.locator(CheckoutLocators.PAY_NOW_BUTTON)).to_be_disabled() 
        self.page.locator(CheckoutLocators.CARD_EXPIRY).fill("1")        
        self.page.locator(CheckoutLocators.CARD_HOLDER_NAME).click()
        self.expect_validation_message("Month must be exactly 2 characters")
        expect(self.page.locator(CheckoutLocators.PAY_NOW_BUTTON)).to_be_disabled()
        self.clear_field("expiry")
        self.page.locator(CheckoutLocators.CARD_EXPIRY).fill("33")        
        self.page.locator(CheckoutLocators.CARD_HOLDER_NAME).click()
        self.expect_validation_message("Please provide a valid expiration month")
        expect(self.page.locator(CheckoutLocators.PAY_NOW_BUTTON)).to_be_disabled()
        self.clear_field("expiry")
        self.page.locator(CheckoutLocators.CARD_EXPIRY).fill("01/2")
        self.page.locator(CheckoutLocators.CARD_HOLDER_NAME).click()
        self.expect_validation_message("Year must be exactly 2 characters")
        expect(self.page.locator(CheckoutLocators.PAY_NOW_BUTTON)).to_be_disabled()
        self.clear_field("expiry")
        self.page.locator(CheckoutLocators.CARD_NUMBER).fill("4111111111111111")
        self.page.locator(CheckoutLocators.CARD_HOLDER_NAME).fill("John Doe")     
        self.page.locator(CheckoutLocators.CARD_CVC).fill("123")
        self.page.locator(CheckoutLocators.CARD_EXPIRY).fill("03/03")
        self.page.locator(CheckoutLocators.PAY_NOW_BUTTON).click()
        self.expect_validation_message("Expiration date must be in the future")         



    def validate_cvc_field(self):
        """Validate CVC field is required"""
        self.page.locator(CheckoutLocators.CARD_NUMBER).fill("4111111111111111")
        self.page.locator(CheckoutLocators.CARD_HOLDER_NAME).fill("John Doe")
        self.page.locator(CheckoutLocators.CARD_EXPIRY).fill("01/29")
        self.page.locator(CheckoutLocators.CARD_CVC).fill("")
        # Click away from the field to trigger validation
        self.page.locator(CheckoutLocators.CARD_EXPIRY).click()
        self.expect_validation_message("This field is required")
        self.clear_field("cvc")
        self.page.locator(CheckoutLocators.CARD_CVC).fill("1")
        self.page.locator(CheckoutLocators.CARD_EXPIRY).click()
        self.expect_validation_message("Security code must be at least 3 characters")
        expect(self.page.locator(CheckoutLocators.PAY_NOW_BUTTON)).to_be_disabled()        
 
        
    def validate_card_number_format(self):
        """Validate card number format"""        
        self.page.locator(CheckoutLocators.CARD_HOLDER_NAME).fill("John Doe")     
        self.page.locator(CheckoutLocators.CARD_CVC).fill("123")
        self.page.locator(CheckoutLocators.CARD_EXPIRY).fill("02/29")
        self.page.locator(CheckoutLocators.CARD_NUMBER).fill("4111")        
        self.expect_validation_message("Card Number must be at least 12 characters")
        expect(self.page.locator(CheckoutLocators.PAY_NOW_BUTTON)).to_be_disabled()

    def clear_field(self, field: str):
        """Clear field"""
        field_locators = {
            "card_number": CheckoutLocators.CARD_NUMBER,
            "card_holder_name": CheckoutLocators.CARD_HOLDER_NAME,
            "expiry": CheckoutLocators.CARD_EXPIRY,
            "cvc": CheckoutLocators.CARD_CVC
        }
        self.page.locator(field_locators[field]).fill("")
        
        
        
        
        
        



