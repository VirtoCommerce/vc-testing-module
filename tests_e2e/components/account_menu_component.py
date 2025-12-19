from re import L
from playwright.sync_api import Locator
from typing import List, Optional

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
 
    
    @property
    def organization_selector_items(self) -> List[Locator]:
        return self.element.locator(
            "[data-test-id^='main-layout.top-header.account-menu.organization-selector-item-']"
        ).all()

    def organization_selector_item(self, organization_name: str) -> Locator:       
        return self.element.locator(
            "[data-test-id^='main-layout.top-header.account-menu.organization-selector-item-']",
            has_text=organization_name,
        )
  

    @property
    def search_organization(self) -> Locator:    
        return (
            self.element.locator(
                "[data-test-id='main-layout.account-menu.top-header.organizations-search']"
            ).locator("input")
        )
    
    @property
    def organization_list(self) -> Locator:
        return self.element.locator(
            "[data-test-id='main-layout.account-menu.top-header.organizations-list']"
        )