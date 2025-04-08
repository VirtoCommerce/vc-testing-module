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


    # Order Details
    ORDER_COMMENTS = "#order_comments"
    
    # Payment Methods
    PAYMENT_METHOD_BUTTON = "//div[@data-test-id='payment-method-select']"
    PAYMENT_METHOD_MANUAL = "//span[contains(.,'{}')]"
    PAYMENT_METHOD_CREDIT_CARD = "//span[contains(.,'Bank card ({})')]"
    
    # Credit Card Fields
    CARD_NUMBER_IFRAME = "iframe[name*='__privateStripeFrame']"
    CARD_NUMBER = "[name='cardnumber']"
    CARD_EXPIRY = "[name='exp-date']"
    CARD_CVC = "[name='cvc']"
    
    # Order Review
    ORDER_REVIEW_TABLE = ".shop_table"
    CART_SUBTOTAL = "tr.cart-subtotal .amount"
    ORDER_TOTAL = "tr.order-total .amount"
    
    # Buttons and Actions
    PROCEED_TO_BILLING_BUTTON = "//button[@data-test-id='proceed-to-button']"
    PROCEED_TO_REVIEW_BUTTON = "//button[@data-test-id='proceed-to-button']"

    
    # Order Confirmation
    ORDER_RECEIVED_MESSAGE = ".woocommerce-thankyou-order-received"
    ORDER_NUMBER = ".woocommerce-order-overview__order strong"
    
    # Error Messages
    ERROR_MESSAGE = ".woocommerce-error"
        