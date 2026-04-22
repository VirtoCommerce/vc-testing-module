import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import HomePage, SignInPage
from playwright.sync_api import Page, expect

_USERNAME = "acme_store_employee_1@acme.com"
_ORIGINAL_ORGANIZATION_NAME = "ACME Store"
_TARGET_ORGANIZATION_NAME = "ACME Store 2"
_SPECIAL_CHAR_ORG_TEST_DATA = [
    ("[e2e] ", "literal brackets"),
    ("(parentheses) ", "parentheses"),
    ("Company & ", "ampersand"),
    ("Test* Des", "asterisk"),
]


@pytest.mark.e2e
@pytest.mark.skip
def test_account_menu_organizations_change(
    global_settings: GlobalSettings,
    page: Page,
) -> None:
    sign_in_page = SignInPage(global_settings=global_settings, page=page)
    sign_in_page.navigate()
    sign_in_page.email_input.fill(_USERNAME)
    sign_in_page.password_input.fill(global_settings.users_password.get_secret_value())
    sign_in_page.sign_in_button.click()

    home_page = HomePage(global_settings=global_settings, page=page)

    expect(home_page.top_header.account_button.customer_name_label).to_be_visible()
    expect(home_page.top_header.account_button.organization_name_label).to_be_visible()
    expect(home_page.top_header.account_button.organization_name_label).to_have_text(_ORIGINAL_ORGANIZATION_NAME)

    home_page.top_header.account_button.root.click()
    expect(home_page.top_header.account_menu.root).to_be_visible()

    home_page.top_header.account_menu.select_organization(name=_TARGET_ORGANIZATION_NAME)
    expect(home_page.top_header.account_button.organization_name_label).to_have_text(_TARGET_ORGANIZATION_NAME)
    home_page.top_header.account_button.root.click()
    home_page.top_header.account_menu.select_organization(name=_ORIGINAL_ORGANIZATION_NAME)


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_user(_USERNAME)
def test_account_menu_organizations_search(
    global_settings: GlobalSettings,
    page: Page,
) -> None:
    home_page = HomePage(global_settings=global_settings, page=page)
    home_page.navigate()

    home_page.top_header.account_button.root.click()
    expect(home_page.top_header.account_menu.root).to_be_visible()
    expect(home_page.top_header.account_menu.search_organizations_input).to_be_visible()
    expect(home_page.top_header.account_menu.search_organizations_button).to_be_visible()

    part_of_org_name = "ACME Store"
    home_page.top_header.account_menu.search_organizations_input.fill(part_of_org_name)
    home_page.top_header.account_menu.search_organizations_button.click()

    expect(home_page.top_header.account_menu.organizations_list.first).to_be_visible()

    orgs = home_page.top_header.account_menu.organizations_list
    names = [orgs.nth(i).get_attribute("data-organization-name") for i in range(orgs.count())]
    assert len(names) > 1, "No search results found (only the pinned current organization)"
    assert all(
        part_of_org_name.lower() in name.lower() for name in names if name
    ), f"Not all organizations contain '{part_of_org_name}': {names}"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_user(_USERNAME)
def test_account_menu_organizations_search_not_found(
    global_settings: GlobalSettings,
    page: Page,
) -> None:
    home_page = HomePage(global_settings=global_settings, page=page)
    home_page.navigate()

    home_page.top_header.account_button.root.click()
    expect(home_page.top_header.account_menu.root).to_be_visible()
    expect(home_page.top_header.account_menu.search_organizations_input).to_be_visible()
    expect(home_page.top_header.account_menu.search_organizations_button).to_be_visible()

    home_page.top_header.account_menu.search_organizations_input.fill("NonExistentOrg")
    home_page.top_header.account_menu.search_organizations_button.click()

    expect(home_page.top_header.account_menu.orgnanizations_empty_list).to_be_visible()


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_user(_USERNAME)
@pytest.mark.parametrize("search_term, char_description", _SPECIAL_CHAR_ORG_TEST_DATA)
def test_account_menu_organizations_search_special_characters(
    global_settings: GlobalSettings,
    page: Page,
    search_term: str,
    char_description: str,
) -> None:
    home_page = HomePage(global_settings=global_settings, page=page)
    home_page.navigate()

    home_page.top_header.account_button.root.click()
    expect(home_page.top_header.account_menu.root).to_be_visible()
    expect(home_page.top_header.account_menu.search_organizations_input).to_be_visible()
    expect(home_page.top_header.account_menu.search_organizations_button).to_be_visible()

    home_page.top_header.account_menu.search_organizations_input.fill(search_term)
    home_page.top_header.account_menu.search_organizations_button.click()
    home_page.top_header.account_menu.wait_for_results()

    orgs = home_page.top_header.account_menu.organizations_list
    expect(orgs.first).to_be_visible()
    names = [orgs.nth(i).get_attribute("data-organization-name") for i in range(orgs.count())]
    assert len(names) > 1, "No search results found (only the pinned current organization)"
    assert any(
        search_term.strip().lower() in name.lower() for name in names if name
    ), f"Expected at least one organization to contain '{search_term.strip()}', got {names}"
