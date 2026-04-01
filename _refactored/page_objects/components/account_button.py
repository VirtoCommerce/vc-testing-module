from playwright.sync_api import Locator

from .component import Component


class AccountButton(Component):
    @property
    def organization_name_label(self) -> Locator:
        return self._root.locator("[data-test-id='organization-name-label']")

    @property
    def customer_name_label(self) -> Locator:
        return self._root.locator("[data-test-id='customer-name-label']")
