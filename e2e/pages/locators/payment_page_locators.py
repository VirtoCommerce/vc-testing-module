class PaymentPageLocators:
    """Locators for payment page elements"""
    # Payment Page
    PAYMENT_PAGE_URL = "/checkout/payment"
    PAYMENT_PAGE_TITLE = "//h1[text()='Payment']"
    PAYMENT_METHOD = "//span[normalize-space(text())='Bank card ({})']"
    PAYMENT_FORM = "(//div[@class='p-5 md:p-6']//div)[2]"

    # CyberSource
  
    CYBERSOURCE_CARD_NUMBER = "//input[@data-test-id='card-number-input']"
    CYBERSOURCE_CARD_HOLDER_NAME = "//input[@data-test-id='card-holder-input']"
    CYBERSOURCE_CARD_EXPIRY = "//input[@data-test-id='expiration-date-input']"
    CYBERSOURCE_CARD_CVC = "//input[@data-test-id='security-code-input']" 
        

    # Credit Card Fields
    CARD_NUMBER = "//input[@data-test-id='card-number-input']"
    CARD_HOLDER_NAME = "//input[@data-test-id='card-holder-input']"
    CARD_EXPIRY = "//input[@data-test-id='expiration-date-input']"
    CARD_CVC = "//input[@data-test-id='security-code-input']"
    PAY_NOW_BUTTON = "//button[@data-test-id='pay-now-button']"

    # Payment Success
    PAYMENT_SUCCESS = "//h1[text()='Payment successful']"
    PAYMENT_SUCCESS_URL = "/checkout/payment/success"
    
    # Payment Failure
    PAYMENT_FAILURE = "//h1[text()='Payment failed']"
    PAYMENT_FAILURE_URL = "/checkout/payment/failure"

    # Show Order
    SHOW_ORDER_BUTTON = "//span[text()='Show order']"
    ERROR_MESSAGE = "//div[@class='vc-input-details__message']"


