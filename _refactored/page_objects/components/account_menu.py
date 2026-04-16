from playwright.sync_api import Locator

from .component import Component


class AccountMenu(Component):
    @property
    def dashboard_link(self) -> Locator:
        return self._root.locator("[data-test-id='dashboard-link']")

    @property
    def sign_out_button(self) -> Locator:
        return self._root.locator("[data-test-id='sign-out-button']")

    @property
    def search_organizations_input(self) -> Locator:
        return self._root.locator("[data-test-id='organizations-search'] input")

    @property
    def search_organizations_button(self) -> Locator:
        return self._root.locator("[data-test-id='organizations-search-button']")

    @property
    def orgnanizations_empty_list(self) -> Locator:
        return self._root.locator("[data-test-id='organizations-empty-list']")

    @property
    def organizations_list(self) -> Locator:
        return self._root.locator("[data-organization-name]")

    def select_organization(self, name: str) -> None:
        organization = self.find_organization(name)
        with self._root.page.expect_navigation(wait_until="load"):
            organization.click()

    def find_organization(self, name: str) -> Locator:
        return self._root.locator(f"[data-organization-name='{name}']")
