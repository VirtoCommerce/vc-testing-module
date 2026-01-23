from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.config import Config
from tests_e2e.pages.home_page import HomePage
from tests_e2e.pages.sign_in_page import SignInPage

EXPECTED_ORGANIZATION_SEARCH_RESULTS = 2


def get_user_organization_count(dataset: dict[str, Any], user: dict[str, Any]) -> int:

    member_id = user.get("memberId")
    if not member_id:
        return 0

    contacts = dataset.get("contacts", [])
    user_contact = next(
        (contact for contact in contacts if contact.get("id") == member_id), None
    )
    return len(user_contact.get("organizations", [])) if user_contact else 0


def assert_organization_count(account_menu_component, expected_count: int) -> None:
    actual_count = len(account_menu_component.organization_selector_items)
    assert (
        actual_count == expected_count
    ), f"Number of organizations is not {expected_count}, but {actual_count}"


@pytest.mark.e2e
@allure.title("Switch between organizations (E2E)")
def test_e2e_switch_between_organizations(
    config: Config, dataset: dict[str, Any], page: Page
):
    with allure.step("Prepare browser and page objects"):
        page.set_viewport_size({"width": 1920, "height": 1080})
        sign_in_page = SignInPage(page, config)
        home_page = HomePage(page, config)

    dataset_user = dataset["users"][0]
    expected_org_count = get_user_organization_count(dataset, dataset_user)

    with allure.step("Sign in and open account menu"):
        sign_in_page.navigate()
        sign_in_page.sign_in(dataset_user["userName"], config["USERS_PASSWORD"])
        account_menu = home_page.open_account_menu()
        assert_organization_count(account_menu, expected_org_count)
        current_organization = home_page.current_organization_name
        first_list_item_name = (
            account_menu.organization_names[0]
            if account_menu.organization_names
            else ""
        )
        assert (
            first_list_item_name == current_organization
        ), f"Current organization '{current_organization}' is not the first in the list (found '{first_list_item_name}')"

        assert (
            len(account_menu.organization_selector_items) == expected_org_count
        ), f"Number of organizations is not {expected_org_count}, but {len(account_menu.organization_selector_items)}"
        expect(account_menu.search_organization).not_to_be_visible()

    with allure.step("Switch to a different organization"):
        for org_name in account_menu.organization_names:
            if org_name == current_organization:
                continue

            account_menu.assert_selection_state(org_name, selected=False)
            account_menu.select_organization(org_name)
            home_page.wait_for_network_idle()

            expect(
                home_page.top_header_component.organization_name_label,
                f"Current organization should be '{org_name}'",
            ).to_have_text(org_name)

            account_menu = home_page.open_account_menu()
            account_menu.assert_selection_state(org_name, selected=True)
            current_organization = home_page.current_organization_name
            first_list_item_name = (
                account_menu.organization_names[0]
                if account_menu.organization_names
                else ""
            )
            assert (
                first_list_item_name == current_organization
            ), f"Current organization '{current_organization}' is not the first in the list (found '{first_list_item_name}')"
            break


@pytest.mark.e2e
@allure.title("Search the organization in the list")
def test_e2e_search_organization_in_list(
    config: Config, dataset: dict[str, Any], page: Page
):
    with allure.step("Prepare browser and page objects"):
        page.set_viewport_size({"width": 1920, "height": 1080})
        sign_in_page = SignInPage(page, config)
        home_page = HomePage(page, config)

    dataset_user = dataset["users"][9]
    organization_name = dataset["organizations"][3]["name"]
    partial_organization_name = dataset["organizations"][5]["name"][:9].lower()
    org_for_switch = dataset["organizations"][10]["name"]
    expected_org_count = get_user_organization_count(dataset, dataset_user)

    with allure.step("Sign in and open account menu"):
        sign_in_page.navigate()
        sign_in_page.sign_in(dataset_user["userName"], config["USERS_PASSWORD"])
        account_menu = home_page.open_account_menu()
        assert_organization_count(account_menu, expected_org_count)
        current_organization = home_page.current_organization_name
        first_list_item_name = (
            account_menu.organization_names[0]
            if account_menu.organization_names
            else ""
        )

        assert (
            first_list_item_name == current_organization
        ), f"Current organization '{current_organization}' is not the first in the list (found '{first_list_item_name}')"

        if len(account_menu.organization_selector_items) > 10:
            expect(
                account_menu.search_organization
            ).to_be_visible(), "Search organization input is not visible when there are more than 10 organizations"
        else:
            expect(
                account_menu.search_organization
            ).not_to_be_visible(), "Search organization input is visible when there are less than 10 organizations"

    with allure.step(f"Search for organization '{organization_name}'"):
        account_menu.search(organization_name)
        expect(account_menu.organization_list).to_be_visible()
        expect(
            account_menu.organization_selector_item(organization_name)
        ).to_contain_text(organization_name)

        current_organization = home_page.current_organization_name
        account_menu.assert_selection_state(current_organization, selected=True)

        filtered_items_count = len(account_menu.organization_selector_items)
        assert (
            filtered_items_count <= 2
        ), f"Number of organizations after search to less than or equal to 2, but {filtered_items_count}"

        assert (
            first_list_item_name == current_organization
        ), f"Current organization '{current_organization}' is not the first in the list (found '{first_list_item_name}')"

        account_menu.search_organization_clear_button.click()
        page.wait_for_timeout(2000)
        account_menu.search(partial_organization_name)
        page.wait_for_timeout(2000)
        expect(account_menu.organization_list).to_be_visible()
        assert (
            len(account_menu.organization_selector_items)
            == EXPECTED_ORGANIZATION_SEARCH_RESULTS
        ), f"Number of organizations after search is not {EXPECTED_ORGANIZATION_SEARCH_RESULTS}, but {len(account_menu.organization_selector_items)}"

    with allure.step(f"Clear search for organization '{organization_name}'"):
        account_menu.search_organization_clear_button.click()
        page.wait_for_timeout(2000)
        expect(account_menu.organization_list).to_be_visible()
        assert (
            len(account_menu.organization_selector_items) == expected_org_count
        ), f"Number of organizations after search is not {expected_org_count}, but {len(account_menu.organization_selector_items)}"

    with allure.step(f"Search for invalid organization name"):
        account_menu.search("Invalid organization name")
        page.wait_for_timeout(2000)
        assert (
            len(account_menu.organization_selector_items) == 0
        ), f"Number of organizations after search is not 0, but {len(account_menu.organization_selector_items)}"
        expect(account_menu.organizations_empty).to_be_visible()
        expect(account_menu.organizations_empty).to_have_text("No results found")
        account_menu.search_organization_clear_button.click()
        page.wait_for_timeout(2000)
        expect(account_menu.organization_list).to_be_visible()

    with allure.step(f"Search for organization name and select it"):
        account_menu.search(org_for_switch)
        page.wait_for_timeout(2000)
        account_menu.organization_selector_item(org_for_switch).click()
        home_page.wait_for_network_idle()
        expect(
            home_page.top_header_component.organization_name_label,
            f"Current organization should be '{org_for_switch}'",
        ).to_have_text(org_for_switch)
        account_menu = home_page.open_account_menu()
        account_menu.assert_selection_state(org_for_switch, selected=True)
        current_organization = home_page.current_organization_name
        assert (
            current_organization == org_for_switch
        ), f"Current organization is not {org_for_switch}, but {current_organization}"

    with allure.step(f"Search for current organization name"):
        account_menu.search(current_organization)
        page.wait_for_timeout(2000)
        assert (
            len(account_menu.organization_selector_items) == 1
        ), f"Number of organizations after search is not 1, but {len(account_menu.organization_selector_items)}"
        expect(
            account_menu.organization_selector_item(current_organization)
        ).to_be_visible()
        account_menu.assert_selection_state(current_organization, selected=True)
        account_menu.search_organization_clear_button.click()
        page.wait_for_timeout(2000)
        expect(account_menu.organization_list).to_be_visible()

    with allure.step("Switch to a different organization"):
        for org_name in account_menu.organization_names:
            if org_name == current_organization:
                continue

            account_menu.assert_selection_state(org_name, selected=False)
            account_menu.select_organization(org_name)
            home_page.wait_for_network_idle()

            expect(
                home_page.top_header_component.organization_name_label,
                f"Current organization should be '{org_name}'",
            ).to_have_text(org_name)

            account_menu = home_page.open_account_menu()
            account_menu.assert_selection_state(org_name, selected=True)
            current_organization = home_page.current_organization_name
            first_list_item_name = (
                account_menu.organization_names[0]
                if account_menu.organization_names
                else ""
            )
            assert (
                first_list_item_name == current_organization
            ), f"Current organization '{current_organization}' is not the first in the list (found '{first_list_item_name}')"
            break
