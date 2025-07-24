from playwright.sync_api import Page, Locator


class CheckoutLayoutPage:
    def __init__(self, page: Page):
        self.page = page

    @property
    def secure_checkout_label(self) -> Locator:
        return self.page.locator("[data-test-id='checkout-layout.secure-checkout-label']")
