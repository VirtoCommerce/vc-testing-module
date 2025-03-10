from .billing_locators import BillingLocators


class BillingPage:
    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.locators = BillingLocators()

    def select_payment_method(self):
        """Select payment method"""
        self.page.get_by_role("button", name="Select a payment method").click()
        self.page.get_by_role("button", name="Account billing").click()

    def proceed_to_review(self):
        """Click proceed to review button"""
        self.page.locator(self.locators.REVIEW_ORDER_BUTTON).click()
        self.page.wait_for_url(f"{self.config['base_url']}/checkout/review")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state("domcontentloaded")
