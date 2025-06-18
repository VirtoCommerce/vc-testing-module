import allure
from playwright.sync_api import Page, BrowserContext, expect
from e2e.pages.locators.saved_credit_card_locators import SavedCreditCardsPageLocators
from utils.dialog_modal_actions import DialogModalActions


class SavedCreditCardsPage:
    def __init__(self, page: Page, config: dict, browser_context: BrowserContext):
        self.page = page
        self.config = config
        self.browser_context = browser_context
        self.dialog_modal_actions = DialogModalActions(self.page)

    def navigate(self):
        """Navigate to saved credit cards page"""
        self.page.goto(f"{self.config['frontend_base_url']}/account/saved-credit-cards")
        self.page.wait_for_load_state("networkidle")
        expect(self.page.locator(SavedCreditCardsPageLocators.SAVED_CREDIT_CARDS_PAGE_TITLE)).to_be_visible()

    def click_saved_credit_cards_link(self):
        """Click saved credit cards"""
        self.page.locator(SavedCreditCardsPageLocators.ACCOUNT_NAVIGATION).click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_url(f"{self.config['frontend_base_url']}/account/saved-credit-cards")
        expect(self.page.locator(SavedCreditCardsPageLocators.SAVED_CREDIT_CARDS_PAGE_TITLE)).to_be_visible()
        self.page.wait_for_load_state("domcontentloaded")

    def check_empty_view(self):
        """Check if the empty view is visible"""
        expect(self.page.locator(SavedCreditCardsPageLocators.SAVED_CREDIT_CARDS_PAGE_TITLE)).to_be_visible()
        expect(self.page.locator(SavedCreditCardsPageLocators.SAVED_CREDIT_CARDS_EMPTY_VIEW)).to_be_visible()

    def check_saved_credit_cards(self):
        """Check if the saved credit cards are visible"""
        expect(self.page.locator(SavedCreditCardsPageLocators.SAVED_CREDIT_CARDS_PAGE_TITLE)).to_be_visible()
        expect(self.page.locator(SavedCreditCardsPageLocators.ALL_CREDIT_CARDS).nth(0)).to_be_attached()
        expect(self.page.locator(SavedCreditCardsPageLocators.ALL_CREDIT_CARDS).nth(0)).to_be_visible()
        count = self.page.locator(SavedCreditCardsPageLocators.ALL_CREDIT_CARDS).count()
        print(f"Found {count} saved credit cards")

    def delete_credit_card(self):
        """Delete credit card"""

        expect(self.page.locator(SavedCreditCardsPageLocators.ALL_CREDIT_CARDS).nth(0)).to_be_attached()
        expect(self.page.locator(SavedCreditCardsPageLocators.ALL_CREDIT_CARDS).nth(0)).to_be_visible()
        self.page.locator(SavedCreditCardsPageLocators.REMOVE_BUTTON).click()
        self.page.wait_for_timeout(1000)
        self.dialog_modal_actions.check_dialog_modal_is_open()
        self.dialog_modal_actions.click_dialog_modal_button_OK()
        self.dialog_modal_actions.check_dialog_modal_is_closed()
        self.page.wait_for_load_state("networkidle")

    def delete_all_credit_cards(self):
        """Delete all saved credit cards"""
        expect(self.page.locator(SavedCreditCardsPageLocators.SAVED_CREDIT_CARDS_PAGE_TITLE)).to_be_visible()
        self.page.wait_for_timeout(1000)

        initial_count = self.page.locator(SavedCreditCardsPageLocators.ALL_CREDIT_CARDS).count()
        print(f"Found {initial_count} credit cards to delete")

        while self.page.locator(SavedCreditCardsPageLocators.ALL_CREDIT_CARDS).count() > 0:
            self.delete_credit_card()

        self.check_empty_view()
        print("All credit cards were successfully removed")
