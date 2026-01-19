from playwright.sync_api import FrameLocator, Locator, Page


class PaymentFormPage:
    # Iframe selector
    IFRAME_SELECTOR = 'iframe[name*="element:group"]'
    
    def __init__(self, page: Page):
        self.page = page

    @property
    def card_number_input(self) -> Locator:
        """Card number input field"""
        return self.page.frame_locator(self.IFRAME_SELECTOR).locator('[id^="element:CARD_NUMBER:"]')

    @property
    def cardholder_name_input(self) -> Locator:
        """Cardholder name input field"""
        return self.page.frame_locator(self.IFRAME_SELECTOR).locator('[id^="element:CARDHOLDER_NAME:"]')

    @property
    def expiry_date_input(self) -> Locator:
        """Expiry date input field"""
        return self.page.frame_locator(self.IFRAME_SELECTOR).locator('[id^="element:EXPIRATION_DATE:"]')

    @property
    def cvv_input(self) -> Locator:
        """Get CVV input within iframe"""
        return self.page.frame_locator(self.IFRAME_SELECTOR).get_by_placeholder("111").nth(1)

    @property
    def loader_spinner(self) -> Locator:
        """Loader spinner"""
        return self.page.locator("[class='vc-loader']")
        
    def fill_card_number(self, card_number: str) -> None:
        """Fill card number field"""
        self.card_number_input.wait_for(state="visible", timeout=30000)
        self.card_number_input.fill(card_number)

    def fill_cardholder_name(self, cardholder_name: str) -> None:
        """Fill cardholder name field"""
        self.cardholder_name_input.wait_for(state="visible", timeout=30000)
        self.cardholder_name_input.fill(cardholder_name)

    def fill_expiry_date(self, expiry_date: str) -> None:
        """Fill expiry date field (format: MM/YY)"""
        self.expiry_date_input.wait_for(state="visible", timeout=30000)
        self.expiry_date_input.fill(expiry_date)

    def fill_cvv(self, cvv: str) -> None:
        """Fill CVV field"""
        self.cvv_input.wait_for(state="visible", timeout=30000)
        self.cvv_input.fill(cvv)

    def fill_payment_form(
        self,
        card_number: str = "4242424242424242",
        expiry_date: str = "12/35",
        cvv: str = "123",
        cardholder_name: str = "TEST"
    ) -> None:
        """Fill all payment form fields in iframe"""
        self.fill_card_number(card_number)
        self.fill_cardholder_name(cardholder_name)
        self.fill_expiry_date(expiry_date)
        self.fill_cvv(cvv)

    def click_pay_now_button(self) -> None:
        """Click pay now button and wait for loader to disappear"""
        self.page.locator('[data-test-id="pay-now-button"]').click()
        self.loader_spinner.wait_for(state="visible", timeout=600000)
        self.loader_spinner.wait_for(state="hidden", timeout=600000)

