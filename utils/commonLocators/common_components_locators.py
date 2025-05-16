class CommonComponentsLocators:
    """Common Components Locators"""
    ADD_TO_CART_BUTTON = "//button[@title='Add to cart']"
    UPDATE_CART_BUTTON = "//button[@title='Update cart']"
    VC_LOADER_OVERLAY_SPINNER = '.vc-loader-overlay__spinner'
    CHECKBOX = "//input[@type='checkbox']"
    DROPDOWN = "(//ul[contains(@class,'vc-dropdown-menu__list')])[{}]"
    DROPDOWN_OPTION = "//li[contains(@class,'vc-dropdown-menu__item') and contains(text(),'{}')]"


