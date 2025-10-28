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
 
    
    def get_radio_button_of_organization(self, organization_name: str) -> Locator:
        return self.element.locator(
            f"div[data-test-id='main-layout.top-header.account-menu.organization-selector-item-{organization_name}'] input"
        )


    def get_organization_selector_item(self, organization_name: str) -> Optional[Locator]:
        for item in self.organization_selector_items:
            attr = item.get_attribute("data-test-id")
            if attr.endswith(f"-{organization_name}"):
                return item
        return None 
