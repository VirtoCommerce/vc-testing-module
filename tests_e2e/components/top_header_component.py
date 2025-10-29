from playwright.sync_api import Locator

from tests_e2e.components.account_menu_component import AccountMenuComponent
from tests_e2e.components.currency_selector_component import CurrencySelectorComponent
from tests_e2e.components.language_selector_component import LanguageSelectorComponent


class TopHeaderComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def language_selector_component(self) -> LanguageSelectorComponent:
        return LanguageSelectorComponent(
            self.element.locator(
                "[data-test-id='main-layout.top-header.language-selector']"
            )
        )

    @property
    def currency_selector_component(self) -> CurrencySelectorComponent:
        return CurrencySelectorComponent(
            self.element.locator(
                "[data-test-id='main-layout.top-header.currency-selector']"
            )
        )

    @property
    def sign_in_link(self) -> Locator:
        return self.element.locator("[data-test-id='sign-in-link']")

    @property
    def sign_up_link(self) -> Locator:
        return self.element.locator("[data-test-id='sign-up-link']")

    @property
    def dashboard_link(self) -> Locator:
        return self.element.locator(
            "[data-test-id='main-layout.top-header.dashboard-link']"
        )

    @property
    def account_menu_button(self) -> Locator:
        return self.element.locator(
            "[data-test-id='main-layout.top-header.account-menu-button']"
        )

    @property
    def account_menu_component(self) -> AccountMenuComponent:
        return AccountMenuComponent(
            self.element.locator("[data-test-id='main-layout.top-header.account-menu']")
        )

    @property
    def account_menu(self) -> Locator:
        return self.element.locator(
            "[data-test-id='main-layout.top-header.account-menu']"
        )

    @property
    def ship_to_selector(self) -> Locator:
        return self.element.locator("[data-test-id='ship-to-selector']")

    @property
    def add_shipping_address_button(self) -> Locator:
        return self.element.locator("[data-test-id='add-shipping-address-button']")
