# Currency test data
CURRENCY_TEST_PRODUCT = {
    "url": "printers/multifunction-printers/laser-color/epson-workforce-wf-3640-all-in-one-printer",
    "name": "ZZZitem for theme performance. Don't delete! Printer Epson",
    "quantity": 2,
    "price": 60.00,
    "url_2": "e2e-test-electronics/e2e-test-asus-expertbook-b5-b5604",
    "name_2": "[E2E Test] ASUS ExpertBook B5 (B5604)",
    "quantity_2": 2,
    "price_2": 1442.99
}

# Merge cart test data
MERGE_CART_USER_PRODUCT = {
    "name": "[E2E Test] ASUS ExpertBook B5 (B5604)",
    "url": "e2e-test-electronics/e2e-test-asus-expertbook-b5-b5604",
    "quantity": 2,
    "price": 1442.99
}

MERGE_CART_ANONYMOUS_PRODUCT = {
    "url": "printers/multifunction-printers/laser-color/epson-workforce-wf-3640-all-in-one-printer",
    "name": "ZZZitem for theme performance. Don't delete! Printer Epson",
    "quantity": 1,
    "price": 60.00
}

SHIPPING_DATA = {
    "first_name": "Admin",
    "last_name": "B2B",
    "email": "admin@b2b.com",
    "phone": "324238423",
    "country": "Hungary",
    "address": "Kossuth Lajos utca 1",
    "city": "Budapest",
    "postcode": "1023"
}

DELIVERY_METHOD1 = "Ground"
DELIVERY_METHOD2 = "Air"

BILLING_DATA = {
    "first_name": "AnnaTab",
    "last_name": "MTab",
    "email": "weiewfoiu@jhkrgh.rgw",
    "phone": "32423",
    "address": "Main street 44",
    "city": "Paris",
    "postcode": "75000"
}

PAYMENT_METHOD1 = "Authorize.Net"
PAYMENT_METHOD2 = "CyberSource"
PAYMENT_METHOD3 = "Skyflow"
PAYMENT_METHOD4 = "Manual"

PAYMENT_DATA = {
    "card_number": "4111111111111111",
    "expiry": "10/29",
    "cvc": "900",
    "card_holder_name": "John Doe"
}

PAYMENT_DATA_FAILED = {
    "card_number": "4007000000027",
    "expiry": "10/29",
    "cvc": "902",
    "card_holder_name": "John Doe"
}
PAYMENT_CYBERSOURCE = {
    "card_number": "4622 9431 2701 3747",
    "expiry": "12/2029",
    "card_holder_name": "John Doe",
    "cvc": "370"
}

PAYMENT_CYBERSOURCE_FAILED = {
    "card_number": "4622 9431 2701 3747",
    "expiry": "12/2022",
    "card_holder_name": "John Doe",
    "cvc": "500"
}

PRODUCT = {
        "url": "printers/multifunction-printers/laser-color/epson-workforce-wf-3640-all-in-one-printer",
        "name": "ZZZitem for theme performance. Don't delete! Printer Epson",
        "initial_quantity": 2,
        "updated_quantity": 3,
        "price": 60.00
    }

ERROR_MESSAGE = {
    "card_number": "This field is required",
    "card_number_format": "Card Number must be at least 12 characters",
    "card_number_valid": "Please provide a valid card number",

    "card_holder_name": "This field is required",
    "card_holder_name_format": "This field must not contain more than 64 characters",

    "expiry": "This field is required",
    "expiry_month_format": "Month must be exactly 2 characters",
    "expiry_year_format": "Year must be exactly 2 characters",
    "cybersource_year_format": "Year must be exactly 4 characters",
    "expiry_month_valid": "Please provide a valid expiration month",
    "expiry_year_valid": "Please provide a valid expiration year",
    
    "expiry_date_valid": "Expiration date must be in the future",
    "expiry_date_format": "Please provide a valid expiration date",
    "expiry_date_valid": "Expiration date must be in the future",

    "cvc": "This field is required",
    "cvc_format": "Security code must be at least 3 characters"
   
    

}




