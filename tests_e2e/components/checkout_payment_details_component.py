from playwright.sync_api import Locator


class CheckoutPaymentDetailsComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def payment_method_selector(self) -> Locator:
        return self.element.locator("[data-test-id='checkout.payment-method-selector']")

    def select_payment_method(self, payment_method: str) -> None:
        self.payment_method_selector.click()
        self.element.locator(f"[data-payment-method-id='{payment_method}']").click()
