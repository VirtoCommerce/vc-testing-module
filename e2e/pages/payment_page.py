from playwright.sync_api import Page, BrowserContext, expect
from utils.commonLocators.common_components_locators import CommonComponentsLocators
from e2e.pages.locators.payment_page_locators import PaymentPageLocators
from e2e.pages.testData.test_data import ERROR_MESSAGE, SKYFLOW_ERROR_MESSAGE, PAYMENT_SKYFLOW

class PaymentPage:
    def __init__(self, page: Page, config: dict, browser_context: BrowserContext):
        self.page = page
        self.config = config
        self.browser_context = browser_context

    def check_payment_page(self, payment_method: str):
        """Check payment page"""
        expect(self.page).to_have_url(self.config["base_url"] + PaymentPageLocators.PAYMENT_PAGE_URL)
        print(f"Payment page URL: {self.config['base_url'] + PaymentPageLocators.PAYMENT_PAGE_URL}")
        self.page.locator(PaymentPageLocators.PAYMENT_PAGE_TITLE).wait_for(state="visible")
        self.page.locator(PaymentPageLocators.PAYMENT_METHOD.format(payment_method)).wait_for(state="visible")
        self.page.locator(PaymentPageLocators.PAYMENT_FORM).wait_for(state="visible")
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")   
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled()
        print(f"Payment form is loaded")

        
    def click_pay_now_button(self):
        """Click on the Pay Now button and wait for the payment to process"""
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_enabled()
        self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON).click()
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")        
    
    def fill_payment_details(self, payment_info: dict):
        """Fill payment details"""
        self.page.locator(PaymentPageLocators.CARD_NUMBER).type(payment_info["card_number"], delay=100)
        self.page.locator(PaymentPageLocators.CARD_HOLDER_NAME).type(payment_info["card_holder_name"], delay=100)
        self.page.locator(PaymentPageLocators.CARD_EXPIRY).type(payment_info["expiry"], delay=100)
        self.page.locator(PaymentPageLocators.CARD_CVC).type(payment_info["cvc"], delay=100)
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_visible()        
        self.click_pay_now_button()
    
    def fill_cybersource_payment_details(self, payment_info: dict):
        """Fill CyberSource payment details"""
        # Get the iframe
        iframe_card_number = self.page.frame_locator("(//iframe)[1]")       
        iframe_card_cvc = self.page.frame_locator("(//iframe)[2]")
     
        # Fill the form inside iframe
        iframe_card_number.locator(PaymentPageLocators.CYBERSOURCE_CARD_NUMBER).type(payment_info["card_number"], delay=100)
        self.page.locator(PaymentPageLocators.CARD_HOLDER_NAME).type(payment_info["card_holder_name"], delay=100)
        self.page.locator(PaymentPageLocators.CARD_EXPIRY).type(payment_info["expiry"], delay=100)
        iframe_card_cvc.locator(PaymentPageLocators.CYBERSOURCE_CARD_CVC).type(payment_info["cvc"], delay=100)
        self.page.locator(PaymentPageLocators.PAYMENT_FORM_CYBERSOURCE).click()     
        self.click_pay_now_button()

    def cybersource_form_validation(self):
        """Cybersource form validation"""
        iframe_card_number = self.page.frame_locator("(//iframe)[1]")       
        iframe_card_cvc = self.page.frame_locator("(//iframe)[2]")
     
        # Fill the form inside iframe
        iframe_card_number.locator(PaymentPageLocators.CYBERSOURCE_CARD_NUMBER).type("4111111111111111", delay=100)
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled()  
        iframe_card_number.locator(PaymentPageLocators.CYBERSOURCE_CARD_NUMBER).type("")
        self.page.locator(PaymentPageLocators.CARD_HOLDER_NAME).type("Joh000++!_____£$%£$^%*", delay=100) 
        self.page.locator(PaymentPageLocators.CARD_EXPIRY).type("8", delay=100)
        self.expect_validation_message(ERROR_MESSAGE["expiry_month_format"])
        self.clear_field("expiry")
        self.page.locator(PaymentPageLocators.CARD_EXPIRY).type("88", delay=100)
        self.expect_validation_message(ERROR_MESSAGE["expiry_month_valid"])
        self.clear_field("expiry")
        self.page.locator(PaymentPageLocators.CARD_EXPIRY).type("01/2", delay=100)
        self.expect_validation_message(ERROR_MESSAGE["cybersource_year_format"])
        self.clear_field("expiry")
        self.page.locator(PaymentPageLocators.CARD_EXPIRY).type("01/0202", delay=100)
        self.expect_validation_message(ERROR_MESSAGE["expiry_year_valid"])
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled()  
        self.clear_field("expiry")
        iframe_card_cvc.locator(PaymentPageLocators.CYBERSOURCE_CARD_CVC).type("123", delay=100)
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled()   
        iframe_card_cvc.locator(PaymentPageLocators.CYBERSOURCE_CARD_CVC).type("")
        iframe_card_cvc.locator(PaymentPageLocators.CYBERSOURCE_CARD_CVC).type("9", delay=100) 
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled()     
       
              
    def expect_validation_message(self, message: str):
        """Verify validation message for a specific field"""       
        validation_message = self.page.locator(PaymentPageLocators.ERROR_MESSAGE)        
        # Verify the validation message text
        expect(validation_message).to_have_text(message)

    def check_payment_success(self):
        """Check payment success"""            
        self.page.locator(PaymentPageLocators.PAYMENT_SUCCESS).wait_for(state="visible")
        expect(self.page).to_have_url(self.config["base_url"] + PaymentPageLocators.PAYMENT_SUCCESS_URL)
        expect(self.page.locator(PaymentPageLocators.SHOW_ORDER_BUTTON)).to_be_visible()
        print(f"Expected result: payment success")


    def check_payment_failure(self):
        """Check payment failure"""        
        self.page.locator(PaymentPageLocators.PAYMENT_FAILURE).wait_for(state="visible")
        expect(self.page).to_have_url(self.config["base_url"] + PaymentPageLocators.PAYMENT_FAILURE_URL)
        print(f"Expected result: payment failure")

    def validate_card_number_field(self):
        """Validate card number field is required"""
        self.page.locator(PaymentPageLocators.CARD_NUMBER).type("000000000000000", delay=100)
        self.page.locator(PaymentPageLocators.PAYMENT_FORM).click()
        self.clear_field("card_number")  
        self.expect_validation_message(ERROR_MESSAGE["card_number"])        
        self.page.locator(PaymentPageLocators.CARD_NUMBER).type("411", delay=100)        
        self.expect_validation_message(ERROR_MESSAGE["card_number_format"])
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled()
 

    def validate_card_holder_name_field(self):
        """Validate card holder name field is required"""
        self.page.locator(PaymentPageLocators.CARD_NUMBER).type("5424000000000015", delay=100)
        self.page.locator(PaymentPageLocators.PAYMENT_FORM).click()
        self.page.locator(PaymentPageLocators.CARD_HOLDER_NAME).type(" ", delay=100)
        self.clear_field("card_holder_name")
        self.page.locator(PaymentPageLocators.CARD_HOLDER_NAME).type("ryr", delay=100)
        self.clear_field("card_holder_name")   
        # Click away from the field to trigger validation
        self.page.locator(PaymentPageLocators.PAYMENT_FORM).click()
        self.expect_validation_message(ERROR_MESSAGE["card_holder_name"])
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled()        
        # Test with more than 64 characters
        self.clear_field("card_holder_name")
        long_name = "A" * 65  # Create a string with 65 characters
        self.page.locator(PaymentPageLocators.CARD_HOLDER_NAME).type(long_name, delay=100)
        self.page.locator(PaymentPageLocators.PAYMENT_FORM).click()
        self.expect_validation_message(ERROR_MESSAGE["card_holder_name_format"])
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled()

    def validate_expiry_field(self):
        """Validate expiry field is required"""
        self.page.locator(PaymentPageLocators.CARD_NUMBER).type("5424000000000015", delay=100)        
        self.page.locator(PaymentPageLocators.CARD_HOLDER_NAME).type("John Doe", delay=100)
        self.page.locator(PaymentPageLocators.CARD_EXPIRY).type("qw/er", delay=100)  
        self.expect_validation_message(ERROR_MESSAGE["expiry_month_valid"])
        self.clear_field("expiry")
        self.expect_validation_message(ERROR_MESSAGE["expiry"])  
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled() 
        self.page.locator(PaymentPageLocators.CARD_EXPIRY).type("1", delay=100)       
        self.expect_validation_message(ERROR_MESSAGE["expiry_month_format"])
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled()
        self.clear_field("expiry")
        self.page.locator(PaymentPageLocators.CARD_EXPIRY).type("33", delay=100)      
        self.expect_validation_message(ERROR_MESSAGE["expiry_month_valid"])
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled()
        self.clear_field("expiry")
        self.page.locator(PaymentPageLocators.CARD_EXPIRY).type("01/2", delay=100)
        self.page.locator(PaymentPageLocators.CARD_HOLDER_NAME).click()
        self.expect_validation_message(ERROR_MESSAGE["expiry_year_format"])
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled()
        self.clear_field("expiry")     
        self.page.locator(PaymentPageLocators.CARD_CVC).type("123", delay=100)
        self.page.locator(PaymentPageLocators.CARD_EXPIRY).type("03/03", delay=100)
        self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON).click()
        self.expect_validation_message(ERROR_MESSAGE["expiry_date_valid"])         



    def validate_cvc_field(self):
        """Validate CVC field is required"""
        self.page.locator(PaymentPageLocators.CARD_NUMBER).type("4111111111111111", delay=100)
        self.page.locator(PaymentPageLocators.CARD_HOLDER_NAME).type("John Doe", delay=100)
        self.page.locator(PaymentPageLocators.CARD_EXPIRY).type("01/29", delay=100)
        self.page.locator(PaymentPageLocators.CARD_CVC).type("1", delay=100)
        self.page.locator(PaymentPageLocators.PAYMENT_FORM).click()       
        self.expect_validation_message(ERROR_MESSAGE["cvc_format"])
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled()     
        self.clear_field("cvc")  
        self.expect_validation_message(ERROR_MESSAGE["cvc"])    
        
        
    def clear_field(self, field: str):
        """Clear field"""  

        field_locators = {
            "card_number": PaymentPageLocators.CARD_NUMBER,            
            "card_holder_name": PaymentPageLocators.CARD_HOLDER_NAME,
            "expiry": PaymentPageLocators.CARD_EXPIRY,
            "cvc": PaymentPageLocators.CARD_CVC
            
        }
        self.page.locator(field_locators[field]).fill("")

    def skyflow_new_form_fill(self,payment_info: dict):
        """Skyflow new form fill"""

        iframe = self.page.frame_locator("(//iframe)[1]")  

        expect(self.page.locator(CommonComponentsLocators.CHECKBOX)).not_to_be_checked()        
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_NUMBER).type(payment_info["card_number"], delay=100)
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_HOLDER_NAME).type(payment_info["card_holder_name"], delay=100)
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_EXPIRY).type(payment_info["expiry"], delay=100)
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_CVC).type(payment_info["cvc"], delay=100) 

    def skyflow_form_validation(self):
        """Skyflow form validation"""
        iframe = self.page.frame_locator("(//iframe)[1]")
        card_input = (iframe.locator(PaymentPageLocators.SKYFLOW_CARD_NUMBER))         
             
        # Card Number Validation
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled() 
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_NUMBER).type("4", delay=100)
        self.page.locator(PaymentPageLocators.SKYFLOW_NEW_FORM).click()
        expect(iframe.locator(PaymentPageLocators.SKYFLOW_CARD_NUMBER_ERROR)).to_contain_text(SKYFLOW_ERROR_MESSAGE["card_number_invalid"])
        card_input.clear()
        self.page.locator(PaymentPageLocators.SKYFLOW_NEW_FORM).click()
        expect(iframe.locator(PaymentPageLocators.SKYFLOW_CARD_NUMBER_ERROR)).to_contain_text(SKYFLOW_ERROR_MESSAGE["card_number_required"])

        # Card Holder Name Validation
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled() 
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_HOLDER_NAME).type("Joh000++!_____£$%£$^%*", delay=100) 
        self.page.locator(PaymentPageLocators.SKYFLOW_NEW_FORM).click()
        expect(iframe.locator(PaymentPageLocators.SKYFLOW_CARD_HOLDER_NAME_ERROR)).to_contain_text(SKYFLOW_ERROR_MESSAGE["card_holder_name_invalid"])
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_HOLDER_NAME).clear()
        self.page.locator(PaymentPageLocators.SKYFLOW_NEW_FORM).click()
        expect(iframe.locator(PaymentPageLocators.SKYFLOW_CARD_HOLDER_NAME_ERROR)).to_contain_text(SKYFLOW_ERROR_MESSAGE["card_holder_name_required"])
        
        # Expiry Validation and CVC Validation
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled() 
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_CVC).type("123", delay=100)
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_EXPIRY).type("09/26", delay=100)
        self.page.locator(PaymentPageLocators.SKYFLOW_NEW_FORM).click()
     
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_EXPIRY).clear()
        self.page.locator(PaymentPageLocators.SKYFLOW_NEW_FORM).click()
        expect(iframe.locator(PaymentPageLocators.SKYFLOW_CARD_EXPIRY_ERROR)).to_contain_text(SKYFLOW_ERROR_MESSAGE["expiry_required"])

        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_CVC).type("888", delay=100)
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_EXPIRY).type("00/00", delay=100)
        self.page.locator(PaymentPageLocators.SKYFLOW_NEW_FORM).click()
        expect(iframe.locator(PaymentPageLocators.SKYFLOW_CARD_EXPIRY_ERROR)).to_contain_text(SKYFLOW_ERROR_MESSAGE["expiry_invalid"])  
      
        
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_EXPIRY).type("01/2", delay=100)
        expect(iframe.locator(PaymentPageLocators.SKYFLOW_CARD_EXPIRY_ERROR)).to_contain_text(SKYFLOW_ERROR_MESSAGE["expiry_invalid"])       
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_EXPIRY).type("01/", delay=100)
        expect(iframe.locator(PaymentPageLocators.SKYFLOW_CARD_EXPIRY_ERROR)).to_contain_text(SKYFLOW_ERROR_MESSAGE["expiry_invalid"])
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_EXPIRY).clear()
        self.page.locator(PaymentPageLocators.SKYFLOW_NEW_FORM).click()
            
       
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled() 
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_EXPIRY).type("09/26", delay=100) 
        self.page.locator(PaymentPageLocators.SKYFLOW_NEW_FORM).click()

        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_CVC).clear()
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_CVC).type("6", delay=100) 
        self.page.locator(PaymentPageLocators.SKYFLOW_NEW_FORM).click()
        expect(iframe.locator(PaymentPageLocators.SKYFLOW_CARD_CVC_ERROR)).to_contain_text(SKYFLOW_ERROR_MESSAGE["cvc_invalid"])   
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_CVC).clear()
        self.page.locator(PaymentPageLocators.SKYFLOW_NEW_FORM).click()
        expect(iframe.locator(PaymentPageLocators.SKYFLOW_CARD_CVC_ERROR)).to_contain_text(SKYFLOW_ERROR_MESSAGE["cvc_required"])
    

    def skyflow_form_partial_fill(self,payment_info: dict):
        """Skyflow form partial fill"""
        iframe = self.page.frame_locator("(//iframe)[1]")
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_NUMBER).type(payment_info["card_number"], delay=100)
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_HOLDER_NAME).type(payment_info["card_holder_name"], delay=100)
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_EXPIRY).type(payment_info["expiry"], delay=100)
        self.page.locator(PaymentPageLocators.SKYFLOW_NEW_FORM).click()
        expect(iframe.locator(PaymentPageLocators.SKYFLOW_CARD_CVC_ERROR)).to_contain_text(SKYFLOW_ERROR_MESSAGE["cvc_required"])
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON)).to_be_disabled() 


    def save_card_checkbox(self):
        """Save card checkbox"""
        expect(self.page.locator(CommonComponentsLocators.CHECKBOX)).not_to_be_checked()
        self.page.locator(CommonComponentsLocators.CHECKBOX).click()
        expect(self.page.locator(CommonComponentsLocators.CHECKBOX)).to_be_checked()
    
    def select_saved_card(self):
        """Select saved card"""
        self.page.locator(PaymentPageLocators.SELECT_SAVED_CREDIT_CARD).click()
        self.page.locator(PaymentPageLocators.DROP_DOWN_LIST).wait_for(state="visible")
        expect(self.page.locator(PaymentPageLocators.ADD_NEW_CREDIT_CARD)).to_be_visible()
        self.page.locator(PaymentPageLocators.SAVED_CREDIT_CARD_ITEM).click()        
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")
        iframe = self.page.frame_locator("(//iframe)[1]")
        expect(iframe.locator(PaymentPageLocators.SKYFLOW_CARD_CVC)).to_be_visible()       
        self.re_enter_cvv(PAYMENT_SKYFLOW["cvc"])
        self.page.locator(PaymentPageLocators.PAY_NOW_TEXT).click()
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")
    
    def re_enter_cvv(self, cvc: str):
        """Re-enter cvv"""
        iframe = self.page.frame_locator("(//iframe)[1]")

        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON_ENABLED)).to_be_disabled()
        iframe.locator(PaymentPageLocators.SKYFLOW_CARD_CVC).type(cvc, delay=100)
        self.page.wait_for_timeout(1000)     
        expect(self.page.locator(PaymentPageLocators.PAY_NOW_BUTTON_ENABLED)).to_be_enabled()
        

    def clear_skyflow_form(self, field: str):
        """Clear skyflow field"""  
        iframe = self.page.frame_locator("(//iframe)[1]")

        field_locators = {
            "card_number": PaymentPageLocators.SKYFLOW_CARD_NUMBER,            
            "card_holder_name": PaymentPageLocators.SKYFLOW_CARD_HOLDER_NAME,
            "expiry": PaymentPageLocators.SKYFLOW_CARD_EXPIRY,
            "cvc": PaymentPageLocators.SKYFLOW_CARD_CVC
            
        }
        iframe.locator(field_locators[field]).clear()   
        
        
        
        
        
        
        
        
        
        



