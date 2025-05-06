class CheckoutLocators:
    """Locators for checkout page elements"""
    
    # Shipping Information
    SHIPING_ADDRESS_BUTTON = "//button[@data-test-id='select-address-button']"    
    FIRST_NAME = "//input[@aria-label='First name']"
    LAST_NAME = "//input[@aria-label='Last name']"
    EMAIL = "//input[@aria-label='Email']"
    PHONE = "//input[@aria-label='Phone']"
    COMPANY = "//input[@aria-label='Company name']"
    COUNTRY = "//input[@placeholder='{}']"
    ADDRESS_1 = "//input[@aria-label='Address']"
    ADDRESS_2 = "//input[@aria-label='Apt., suite, building number, etc.']"
    CITY = "//input[@aria-label='City']"
    STATE = "//input[@aria-label='State']"
    POSTCODE = "//input[@aria-label='ZIP / Postal code']"

    DELIVERY_METHOD_BUTTON = "//div[@data-test-id='shipping-method-select']"
    DELIVERY_METHOD_FIXED_RATE = "//span[contains(.,'Fixed Rate ({})')]" 
    SELECT_SHIPING_ADDRESS = "(//span[text()='Select'])[1]"
    SELECTED_SHIPPING_ADDRESS = "(//div[@class='vc-address-selection']//span)[1]"

    # Order Details
    ORDER_COMMENTS = "#order_comments"
    
    # Payment Methods
    PAYMENT_METHOD_BUTTON = "//div[@data-test-id='payment-method-select']"
    PAYMENT_METHOD_MANUAL = "//span[contains(.,'{}')]"
    PAYMENT_METHOD_CREDIT_CARD = "//span[contains(.,'Bank card ({})')]"
    
    # Order Review
    ORDER_REVIEW_WIDGET = "(//div[@class='vc-widget__slot']//div)[1]"
    CART_SUBTOTAL = "tr.cart-subtotal .amount"
    ORDER_TOTAL = "tr.order-total .amount"
    ORDER_REVIEW_ITEMS = "//div[@class='vc-line-items']"    
    
    # Buttons and Actions
    PROCEED_TO_BILLING_BUTTON = "//button[@data-test-id='proceed-to-button']"
    PROCEED_TO_REVIEW_BUTTON = "//button[@data-test-id='proceed-to-button']"

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

        