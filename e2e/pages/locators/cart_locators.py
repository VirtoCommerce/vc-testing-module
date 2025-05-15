class CartLocators:
    # Base locators
    LINE_ITEM = "//div[@class='vc-product-title vc-product-title--link vc-line-item__name']"
    PRODUCT_TITLE = "(//a[contains(@title, '{}')])[{}]" 
    # Price locators - relative to LINE_ITEM
    PRICE_LIST = "//span[@class='vc-product-price__actual']/following-sibling::span[1]"
    
    # Other locators...
    CART_ITEM = "//div[@class='vc-line-item__main']"
    CART_ITEM_1 = "(//div[@class='vc-line-item__main'])[{}]"
    QUANTITY_INPUT = "(//input[@aria-label='Product quantity'])[1]"
    ADD_TO_CART_BUTTON = "(//button[@title='Add to cart'])[2]"

    CART_ICON = "//a[@href='/cart']"
    CART_TITLE = "//h1[text()='Cart']"
    CART_LAYOUT = "//div[@id='products']"
    CLEAR_CART_BUTTON = "//span[text()='Clear cart']"
    EMPTY_CART_MESSAGE = "//div[normalize-space(text())='Your cart is empty']" 
    CART_COUNT = "//span[text()='{}']"
    BUTTON_YES = "//span[text()='Yes']"
    DIALOG_MODAL = "//div[@class='vc-dialog']"
    PRICE_ACTUAL_CART_ITEM_1 = "(//span[@class='vc-product-price__actual']//span)[{}]"   
    MAX_QUANTITY_ERROR = "//div[normalize-space(text())='You can order maximum 20 item(s)']"
    PROCEED_TO_BUTTON = "(//a[@data-test-id='proceed-to-button'][@disabled='false'])[1]"
    PROCEED_TO_BUTTON_DISABLED = "(//button[@data-test-id='proceed-to-button']//span)[1]"


    SUBTOTAL = "(//div[contains(@class,'mb-4 flex')]//span)[3]"
    TOTAL= "//span[@class='text-[--price-color] print:text-inherit']//span[1]"
    
    # Checkbox locators for selecting/unselecting items
    ITEM_CHECKBOX = "//input[@data-test-id='vc-line-item-checkbox']"
    CHECKED_ITEM_CHECKBOX = "//input[@data-test-id='vc-line-item-checkbox' and @checked]"
    UNCHECKED_ITEM_CHECKBOX = "//input[@data-test-id='vc-line-item-checkbox' and not(@checked)]"
    HEAD_CHECKBOX = "//input[@data-test-id='vc-line-items-head-checkbox']"
    CURRENCY_SELECTOR = "//div[contains(@class, 'vc-currency-selector')]"   
