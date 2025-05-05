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


    def check_payment_success(self):
        """Check payment success"""
        try:
            self.page.wait_for_timeout(10000)
            self.page.locator(CheckoutLocators.PAYMENT_SUCCESS).wait_for(state="visible")
            expect(self.page).to_have_url(self.config["base_url"] + CheckoutLocators.PAYMENT_SUCCESS_URL)
            expect(self.page.locator(CheckoutLocators.SHOW_ORDER_BUTTON)).to_be_visible()
            print(f"Payment success")
        except Exception as e:            
            print(f"Payment failed: {e}")

    def check_payment_failure(self):
        """Check payment failure"""
        self.page.locator(CheckoutLocators.PAYMENT_FAILURE).wait_for(state="visible")
        print(f"Payment failure")
