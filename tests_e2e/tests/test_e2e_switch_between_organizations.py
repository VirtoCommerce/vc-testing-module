import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.config import Config
from tests_e2e.pages.home_page import HomePage
from tests_e2e.pages.sign_in_page import SignInPage


@pytest.mark.e2e
@allure.title("Switch between organizations (E2E)")
def test_e2e_switch_between_organizations(
    config: Config, dataset: dict[str, Any], page: Page
):
    print(f"{os.linesep}Running E2E test to switch between organizations...", end=" ")

    page.set_viewport_size({"width": 1920, "height": 1080})

    sign_in_page = SignInPage(page, config)
    home_page = HomePage(page, config)

    dataset_user = dataset["users"][9]

    sign_in_page.navigate()

    sign_in_page.sign_in(dataset_user["userName"], config["USERS_PASSWORD"])
    organization_selector = home_page.top_header_component.account_menu_component

    home_page.top_header_component.account_menu_button.click()
    expect(
        home_page.top_header_component.account_menu
    ).to_be_visible(), "Account menu is not visible"

    number_of_organizations = len(organization_selector.organization_selector_items)
    assert (
        number_of_organizations == 3
    ), f"Number of organizations is not 3, but {number_of_organizations}"

    current_organization = (
        home_page.top_header_component.organization_name_label.text_content()
    )
    print(f"Current organization is {current_organization}")
    for organization in organization_selector.organization_selector_items:
        if organization.text_content() == current_organization:
            expect(organization.locator("input")).to_have_attribute(
                "aria-checked", "true"
            ), f"Organization '{organization.text_content()}' is not selected"

    # Get all organization locators
    organization_items = organization_selector.organization_selector_items
    current_name = current_organization

    for organization in organization_items:
        org_name = organization.text_content().strip()

        if org_name != current_name:
            selected_organization = organization

            # Check it's not already selected
            expect(
                selected_organization.locator("input"),
                f"Organization '{org_name}' is already selected",
            ).to_have_attribute("aria-checked", "false")

            # Click to select
            selected_organization.locator("input").click()
            page.wait_for_load_state("networkidle")

            # Reopen the account menu to verify selection
            home_page.top_header_component.account_menu_button.click()

            # Verify current organization name
            expect(
                home_page.top_header_component.organization_name_label,
                f"Current organization should be '{org_name}'",
            ).to_have_text(org_name)

            assert (
                selected_organization.text_content().strip() == org_name
            ), f"Current organization should be '{org_name}'"

            # Verify aria-checked updated
            expect(
                selected_organization.locator("input"),
                f"Organization '{org_name}' did not become selected",
            ).to_have_attribute("aria-checked", "true")

            break
