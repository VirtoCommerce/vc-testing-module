class SavedCreditCardsPageLocators:
    """Saved Credit Cards Page Locators"""

    SAVED_CREDIT_CARDS_PAGE_TITLE = "//h1[text()='Saved credit cards']"
    SAVED_CREDIT_CARDS_EMPTY_VIEW = "//div[normalize-space(text())='You have not saved any credit cards yet']"
    SAVED_CREDIT_CARDS_LINK = "//a[@href='/account/saved-credit-cards']"
    ACCOUNT_NAVIGATION = "//span[text()='Saved credit cards']"
    CREDIT_CARD_FIELD = "(//div[@class='credit-card'])[{}]"
    ALL_CREDIT_CARDS = "//div[@class='credit-card']"
    REMOVE_BUTTON = "(//button[@aria-label='Remove credit card'])[1]"
