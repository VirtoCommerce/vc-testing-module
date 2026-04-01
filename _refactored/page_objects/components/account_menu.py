from playwright.sync_api import Locator

from .component import Component


class AccountMenu(Component):
    @property
    def dashboard_link(self) -> Locator:
        return self._root.locator("[data-test-id='dashboard-link']")

    @property
    def sign_out_button(self) -> Locator:
        return self._root.locator("[data-test-id='sign-out-button']")
