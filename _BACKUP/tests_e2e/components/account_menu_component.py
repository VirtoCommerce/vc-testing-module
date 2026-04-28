import re
from typing import List

from playwright.sync_api import Locator, expect


class AccountMenuComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def dashboard_link(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.top-header.account-menu.dashboard-link']")

    @property
    def sign_out_button(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.top-header.account-menu.sign-out-button']")

    @property
    def organization_selector_items(self) -> List[Locator]:
        return self.element.locator(
            "[data-test-id^='main-layout.top-header.account-menu.organization-selector-item-']"
        ).all()

    def organization_selector_item(self, organization_name: str) -> Locator:
        exact_text = re.compile(f"^{re.escape(organization_name)}$")
        return self.element.locator(
            "[data-test-id^='main-layout.top-header.account-menu.organization-selector-item-']",
            has_text=exact_text,
        )

    @property
    def search_organization(self) -> Locator:
        return self.element.locator(
            "[data-test-id='main-layout.account-menu.top-header.organizations-search']"
        ).locator("input")

    @property
    def organizations_empty(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.top-header.account-menu.organizations-empty']")

    @property
    def search_organization_clear_button(self) -> Locator:
        return self.element.locator(".vc-input__clear button, button.vc-input__clear").first

    @property
    def organization_list(self) -> Locator:
        return self.element.locator("[data-test-id='main-layout.account-menu.top-header.organizations-list']")

    @property
    def organization_names(self) -> List[str]:
        return [(item.text_content() or "").strip() for item in self.organization_selector_items]

    def search(self, value: str) -> None:
        self.search_organization.fill(value)
        self.search_organization.press("Enter")

    def assert_selection_state(self, organization_name: str, *, selected: bool) -> None:
        item = self.organization_selector_item(organization_name)
        if selected:
            expect(
                item,
                f"Organization '{organization_name}' should be selected",
            ).to_have_class(re.compile(r"vc-radio-button--checked"))
        else:
            expect(
                item,
                f"Organization '{organization_name}' should not be selected",
            ).not_to_have_class(re.compile(r"vc-radio-button--checked"))

    def select_organization(self, organization_name: str) -> None:
        self.organization_selector_item(organization_name).click()
