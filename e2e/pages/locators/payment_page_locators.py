class PaymentPageLocators:
    """Locators for payment page elements"""

    # Payment Page
    PAYMENT_PAGE_URL = "/checkout/payment"
    PAYMENT_PAGE_TITLE = "//h1[text()='Payment']"
    PAYMENT_METHOD = "//span[normalize-space(text())='Bank card ({})']"
    PAYMENT_FORM = "(//div[@class='p-5 md:p-6']//div)[2]"
    PAYMENT_FORM_CYBERSOURCE = "//div[@class='form-group']"

    # CyberSource

    CYBERSOURCE_CARD_NUMBER = "//input[@id='number']"
    CYBERSOURCE_CARD_CVC = "//input[@id='securityCode']"

    # Skyflow
    SKYFLOW_NEW_FORM = "//div[@class='p-5 md:p-6']"
    SKYFLOW_CARD_NUMBER = "//input[@data-row-id='row-0']"
    SKYFLOW_CARD_HOLDER_NAME = "//input[@data-row-id='row-1']"
    SKYFLOW_CARD_EXPIRY = "//input[@name='card_expiration']"
    SKYFLOW_CARD_CVC = "//input[@name='cvv']"

    # Credit Card Fields
    CARD_NUMBER = "//input[@data-test-id='card-number-input']"
    CARD_HOLDER_NAME = "//input[@data-test-id='card-holder-input']"
    CARD_EXPIRY = "//input[@data-test-id='expiration-date-input']"
    CARD_CVC = "//input[@data-test-id='security-code-input']"
    PAY_NOW_BUTTON = "//button[@data-test-id='pay-now-button']"
    PAY_NOW_TEXT = "(//span[text()='Pay now'])[1]"
    PAY_NOW_BUTTON_ENABLED = "(//button[@type='button'])[3]"

    # Payment Success
    PAYMENT_SUCCESS = "//h1[text()='Payment successful']"
    PAYMENT_SUCCESS_URL = "/checkout/payment/success"

    # Payment Failure
    PAYMENT_FAILURE = "//h1[text()='Payment failed']"
    PAYMENT_FAILURE_URL = "/checkout/payment/failure"

    # Show Order
    SHOW_ORDER_BUTTON = "//span[text()='Show order']"
    ERROR_MESSAGE = "//div[@class='vc-input-details__message']"

    # Skyflow Error Messages
    SKYFLOW_CARD_NUMBER_ERROR = "//span[@id='row-0-error']"
    SKYFLOW_CARD_HOLDER_NAME_ERROR = "//span[@id='row-1-error']"
    SKYFLOW_CARD_EXPIRY_ERROR = "//span[@id='row-2-error']"
    SKYFLOW_CARD_CVC_ERROR = "//span[@id='row-2-error']"
    SELECT_SAVED_CREDIT_CARD = "(//div[@class='vc-dropdown-menu__trigger']//div)[1]"
    SAVED_CREDIT_CARD_ITEM = "(//span[@class='vc-menu-item__content'])[1]"
    ADD_NEW_CREDIT_CARD = "//span[contains(.,'Add new card')]"
    DROP_DOWN_LIST = "//ul[contains(@class, 'vc-dropdown-menu__list')]"
