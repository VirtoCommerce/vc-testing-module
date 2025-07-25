from playwright.sync_api import Locator


class AccountMenuComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def dashboard_link(self) -> Locator:
        return self.element.locator(
            "[data-test-id='main-layout.top-header.account-menu.dashboard-link']"
        )

    @property
    def sign_out_button(self) -> Locator:
        return self.element.locator(
            "[data-test-id='main-layout.top-header.account-menu.sign-out-button']"
        )
