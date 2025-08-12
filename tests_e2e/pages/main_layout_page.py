from playwright.sync_api import Page

from tests_e2e.components import TopHeaderComponent


class MainLayoutPage:
    def __init__(self, page: Page):
        self.page = page

    @property
    def top_header_component(self) -> TopHeaderComponent:
        return TopHeaderComponent(
            self.page.locator("[data-test-id='main-layout.top-header']")
        )

    def change_language(self, language: str) -> None:
        self.top_header_component.language_selector_component.element.click()

        language_item = self.top_header_component.language_selector_component.get_language_menu_item(
            language
        )

        if not language_item:
            raise ValueError(f"Language item with language '{language}' not found")

        language_item.click()
        self.page.wait_for_load_state("networkidle")

    def change_currency(self, currency: str) -> None:
        self.top_header_component.currency_selector_component.element.click()

        currency_item = self.top_header_component.currency_selector_component.get_currency_menu_item(
            currency
        )

        if not currency_item:
            raise ValueError(f"Currency item with currency '{currency}' not found")

        currency_item.click()
        self.page.wait_for_load_state("networkidle")

    def sign_out(self) -> None:
        self.top_header_component.account_menu_button.click()
        self.top_header_component.account_menu_component.sign_out_button.click()
        self.page.wait_for_load_state("networkidle")
