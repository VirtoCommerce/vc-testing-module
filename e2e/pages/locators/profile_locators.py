class ProfileLocators:
    CURRENCY_SELECTOR = "(//div[@class=\"vc-dropdown-menu__trigger\"])[5]"
    LANGUAGE_SELECTOR = "(//div[@class=\"vc-dropdown-menu__trigger\"])[4]"
    UPDATE_BUTTON = "//span[text()='Update']"
    PROFILE_PAGE_TITLE = "//h1[normalize-space(text())='Profile']"
    DIALOG_MODAL = "//h2[@data-headlessui-state='open']"
    BUTTON_OK = "//span[text()='OK']"
    PROFILE_LINK = "(//span[@class='account-navigation-item__text'])[2]"
    CURRENCY_SELECTOR_OPTION = "//div[2]/div/div[2]/div[2]/ul/li[5]/button/span[2]"
    DEFAULT_CURRENCY = "//input[@placeholder=\"{}\"]"
 
