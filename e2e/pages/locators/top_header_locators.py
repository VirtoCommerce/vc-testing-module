class TopHeaderLocators:
    CURRENCY_SELECTOR_STORE = "//span[@class='uppercase text-[--header-top-link-color] hover:text-[--header-top-link-hover-color]']"
    LANGUAGE_SELECTOR_STORE = "//div[@class='vc-language-selector']"
    UPDATE_BUTTON = "//button[normalize-space(text())='UPDATE']"
    CURRENCY_SELECTOR = "//div[@class='vc-currency-selector']"
    LANGUAGE_SELECTOR = "//div[@class='vc-language-selector']"
    DASHBOARD_LINK = "(//a[@class='top-header-link'])[1]"
    ACCOUNT_LINK = "//a[@href='/account']"
    ORDERS_LINK = "//a[@href='/orders']"
    ADDRESSES_LINK = "//a[@href='/addresses']"   
    LOGOUT_LINK = "//a[@href='/logout']"
    CART_LINK = "//a[@href='/cart']"
    LOGIN_LINK = "(//a[@class='top-header-link'])[2]"


