from playwright.sync_api import Page, expect

from tests_e2e.components import (
    AccountMenuComponent,
    SearchBarComponent,
    TopHeaderComponent,
)


class MainLayoutPage:
    def __init__(self, page: Page):
        self.page = page

    @property
    def top_header_component(self) -> TopHeaderComponent:
        return TopHeaderComponent(
            self.page.locator("[data-test-id='main-layout.top-header']")
        )

    @property
    def account_menu(self) -> AccountMenuComponent:
        return self.top_header_component.account_menu_component

    @property
    def search_bar(self) -> SearchBarComponent:
        return SearchBarComponent(self.page.locator(".search-bar"))

    def dismiss_blocking_modal(self) -> None:
        modal_wrapper = self.page.locator(".vc-modal__wrapper")
        try:
            if modal_wrapper.is_visible():
                # Attempt to close any overlaying modal (e.g., headlessui portals)
                self.page.keyboard.press("Escape")
                modal_wrapper.first.wait_for(state="hidden", timeout=2_000)
        except Exception:
            # Best-effort cleanup; do not fail test flow if the modal persists
            pass

    def open_account_menu(self) -> AccountMenuComponent:
        self.dismiss_blocking_modal()
        self.top_header_component.account_menu_button.click()
        expect(
            self.account_menu.organization_list, "Organization list is not visible"
        ).to_be_visible()
        self.page.wait_for_load_state("networkidle")
        return self.account_menu

    @property
    def current_organization_name(self) -> str:
        name = self.top_header_component.organization_name_label.text_content()
        return name.strip() if name else ""

    def wait_for_network_idle(self) -> None:
        self.page.wait_for_load_state("networkidle")

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
