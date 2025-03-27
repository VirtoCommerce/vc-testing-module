from playwright.sync_api import Page, expect

class CheckoutPage:
    def __init__(self, page: Page, config: dict):
        self.page = page
        self.config = config

    def select_delivery_method(self):
        """Select delivery method"""
        self.page.click("text=Select a delivery method")
        self.page.click("text=Fixed Rate (Ground)")

    def fill_shipping_address(self, data: dict):
        """Fill shipping address form"""
        self.page.click("[data-test-id='select-address-button']")
        self.page.fill("#input-1743", data["first_name"])
        self.page.fill("#input-1746", data["last_name"])
        self.page.fill("#input-1749", data["email"])
        self.page.fill("#input-2012", data["phone"])
        self.page.fill("#input-2023", data["address"])
        self.page.fill("#input-2026", data["city"])

    def proceed_to_billing(self):
        """Proceed to billing"""
        self.page.click("text=PROCEED TO BILLING")

    def select_payment_method(self):
        """Select payment method"""
        self.page.click("text=Select a payment method")
        self.page.click("text=Bank card (CyberSource)")

    def proceed_to_review(self):
        """Proceed to review"""
        self.page.click("text=REVIEW ORDER")

    def place_order(self):
        """Place order"""
        self.page.click("text=PLACE ORDER")

    def expect_completed_order(self):
        """Verify order completion"""
        expect(self.page).to_have_url(f"{self.config['base_url']}/checkout/completed") 