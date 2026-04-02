from playwright.sync_api import Locator

from .account_button import AccountButton
from .account_menu import AccountMenu
from .component import Component
from .currency_selector import CurrencySelector
from .language_selector import LanguageSelector
from .ship_to_selector import ShipToSelector


class TopHeader(Component):
    @property
    def language_selector(self) -> LanguageSelector:
        return LanguageSelector(
            root=self._root.locator("[data-test-id='language-selector']")
        )

    @property
    def currency_selector(self) -> CurrencySelector:
        return CurrencySelector(
            root=self._root.locator("[data-test-id='currency-selector']")
        )

    @property
    def dashboard_link(self) -> Locator:
        return self._root.locator("[data-test-id='dashboard-link']")

    @property
    def contacts_link(self) -> Locator:
        return self._root.locator("[data-test-id='contacts-link']")

    @property
    def support_phone_link(self) -> Locator:
        return self._root.locator("[data-test-id='support-phone-link']")

    @property
    def contact_us_link(self) -> Locator:
        return self._root.locator("[data-test-id='contact-us-link']")

    @property
    def operator_name_label(self) -> Locator:
        return self._root.locator("[data-test-id='operator-name-label']")

    @property
    def sign_in_link(self) -> Locator:
        return self._root.locator("[data-test-id='sign-in-link']")

    @property
    def sign_up_link(self) -> Locator:
        return self._root.locator("[data-test-id='sign-up-link']")

    @property
    def account_button(self) -> AccountButton:
        return AccountButton(root=self._root.locator("[data-test-id='account-button']"))

    @property
    def account_menu(self) -> AccountMenu:
        return AccountMenu(root=self._root.locator("[data-test-id='account-menu']"))

    @property
    def add_shipping_address_button(self) -> Locator:
        return self._root.locator("[data-test-id='add-shipping-address-button']")

    @property
    def ship_to_selector(self) -> ShipToSelector:
        return ShipToSelector(
            root=self._root.locator("[data-test-id='ship-to-selector']")
        )
