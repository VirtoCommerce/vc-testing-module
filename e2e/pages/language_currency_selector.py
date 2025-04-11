from playwright.sync_api import Page, expect
from e2e.pages.locators.top_header_locators import TopHeaderLocators
from e2e.pages.locators.cart_locators import CartLocators
from playwright.sync_api import BrowserContext

class LanguageCurrencySelector:
    def __init__(self, page: Page, browser_context: BrowserContext):
        self.page = page
        self.browser_context = browser_context

    def change_language(self, language: str):
        self.page.click(TopHeaderLocators.LANGUAGE_SELECTOR_STORE)
        self.page.click(f"text={language}")


    def change_currency(self, currency: str):
        self.page.click(TopHeaderLocators.CURRENCY_SELECTOR_STORE)
        self.page.click(f"text={currency}")
    
    def expect_language_change(self, language: str):
        expect(self.page.locator(TopHeaderLocators.LANGUAGE_SELECTOR_STORE)).to_have_text(language)
        print(f"Language changed to {language}")

    def expect_currency_change(self, currency: str):
        expect(self.page.locator(TopHeaderLocators.CURRENCY_SELECTOR_STORE)).to_have_text(currency)
        print(f"Currency changed to {currency}")
    
   

