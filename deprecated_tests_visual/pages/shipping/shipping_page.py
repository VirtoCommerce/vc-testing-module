from .shipping_locators import ShippingLocators


class ShippingPage:
    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.locators = ShippingLocators()

    def select_delivery_method(self):
        """Select delivery method and wait for UI update"""
        self.page.get_by_role("button", name=self.locators.DELIVERY_METHOD_DROPDOWN).click()
        self.page.get_by_role("button", name=self.locators.DELIVERY_METHOD_OPTION).click()
        self.page.wait_for_timeout(2000)
        # Wait for proceed button to become enabled, indicating selection was applied

    def proceed_to_billing(self):
        """Click proceed to billing button"""
        self.page.locator(self.locators.PROCEED_TO_BILLING_BUTTON).click()
        self.page.wait_for_url(f"{self.config['base_url']}/checkout/billing")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state("domcontentloaded")
