from playwright.sync_api import Locator
from tests_e2e.components.currency_selector_component import CurrencySelectorComponent
from tests_e2e.components.language_selector_component import LanguageSelectorComponent


class TopHeaderComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def language_selector_component(self) -> LanguageSelectorComponent:
        return LanguageSelectorComponent(self.element.locator("[data-test-id='main-layout.top-header.language-selector']"))

    @property
    def currency_selector_component(self) -> CurrencySelectorComponent:
        return CurrencySelectorComponent(self.element.locator("[data-test-id='main-layout.top-header.currency-selector']"))

    @property
    def contacts_link(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.top-header.contacts-link']")

    @property
    def sign_in_link(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.top-header.sign-in-link']")

    @property
    def sign_up_link(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.top-header.sign-up-link']")

    @property
    def dashboard_link(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.top-header.dashboard-link']")

    @property
    def account_menu_button(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.top-header.account-menu-button']")

    @property
    def account_menu(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.top-header.account-menu']")