class CartLocators:
    # Base locators
    LINE_ITEM = "//div[@class='vc-line-item__main']"
    PRODUCT_TITLE = "(//a[@title=\"{}\"])[{}]"  # Requires formatting with product name
     # Price locators - relative to LINE_ITEM
    PRICE_ACTUAL = ".//span[@class='vc-product-price__actual']//span[last()]"  # Using relative path with last() instead of fixed index
    # Other locators...
    CART_ITEM = "//div[@class='vc-line-item__main']"
    CART_ITEM_1 = "(//div[@class='vc-line-item__main'])[{}]"
    QUANTITY_INPUT = "(//input[@aria-label='Product quantity'])[1]"
    ADD_TO_CART_BUTTON = "(//button[@title='Add to cart'])[2]"
    CART_ICON = "//a[@href='/cart']"
    CLEAR_CART_BUTTON = "//span[text()='Clear cart']"
    EMPTY_CART_MESSAGE = "//div[normalize-space(text())='Your cart is empty']"    
    CART_COUNT = "//span[text()='{}']"
    BUTTON_YES = "//span[text()='Yes']"
    DIALOG_MODAL = "//div[@class='vc-dialog']"
    PRICE_ACTUAL_CART_ITEM_1 = "(//span[@class='vc-product-price__actual']//span)[{}]"
    PRODUCT_ROW = "//div[@class='vc-line-item__main']"