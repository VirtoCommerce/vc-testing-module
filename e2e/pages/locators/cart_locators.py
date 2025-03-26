class CartLocators:
   
    CART_ITEM = "(//div[@class='vc-line-item__main'])[1]"
    PRODUCT_TITLE = "(//a[@title=\"{}\"])[1]"  # Requires formatting with product name
    QUANTITY_INPUT = "(//input[@aria-label='Product quantity'])[1]"
    ADD_TO_CART_BUTTON = "(//button[@title='Add to cart'])[2]"
    CART_ICON = "//a[@href='/cart']"
    CLEAR_CART_BUTTON = "//span[text()='Clear cart']"
    EMPTY_CART_MESSAGE = "//div[normalize-space(text())='Your cart is empty']"    
    PRICE_ACTUAL = "(//span[@class='vc-product-price__actual']//span)[3]"    
    CART_COUNT = "//span[text()='{}']"
    BUTTON_YES = "//span[text()='Yes']"
    DIALOG_MODAL = "//div[@class='vc-dialog']"