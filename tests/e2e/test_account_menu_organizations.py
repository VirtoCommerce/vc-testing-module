import re
from typing import Any, Callable

import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import HomePage, SignInPage
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect

_USERNAME = "acme_store_employee_1@acme.com"
_ORIGINAL_ORGANIZATION_NAME = "ACME Store"
_TARGET_ORGANIZATION_NAME = "ACME Store 2"
_TARGET_ORGANIZATION_ID = "organization-acme-store-2"
_SPECIAL_CHAR_ORG_TEST_DATA = [
    ("[e2e] ", "literal brackets"),
    ("(parentheses) ", "parentheses"),
    ("Company & ", "ampersand"),
    ("Test* Des", "asterisk"),
]


def _sign_in(global_settings: GlobalSettings, page: Page) -> None:
    """Fresh UI sign-in — locking a membership terminates ALL of the user's sessions
    (RevokeTokenOrganizationMembershipChangedEventHandler). Callers must NOT carry the
    `with_user` marker: it makes autouse `with_cart` sign in via `BrowserStorage.set_auth`,
    which uses `page.add_init_script` — that re-injects the (now-stale) token on every
    navigation for the rest of the page's life, including this one, so the app keeps
    treating the browser as already authenticated and never reaches the sign-in form."""
    sign_in_page = SignInPage(global_settings=global_settings, page=page)
    sign_in_page.navigate()
    sign_in_page.email_input.fill(_USERNAME)
    sign_in_page.password_input.fill(global_settings.users_password.get_secret_value())
    sign_in_page.sign_in_button.click()
    _dismiss_password_expiry_modal(page)


def _dismiss_password_expiry_modal(page: Page) -> None:
    """This seeded user's password is close to expiring, which pops up a "Password is about
    to expire" modal on sign-in — unrelated to VCST-5317, but it intercepts clicks on the
    header underneath it until dismissed. No-op if it doesn't appear."""
    try:
        page.get_by_role("button", name="Cancel").click(timeout=3000)
    except PlaywrightTimeoutError:
        pass


def _employee_1_organization_ids(dataset: dict[str, list[dict[str, Any]]]) -> list[str]:
    contact = next(c for c in dataset["contacts"] if c["id"] == "contact-acme-store-employee-1")
    return list(contact["organizations"])


def _employee_1_user_id(dataset: dict[str, list[dict[str, Any]]]) -> str:
    user = next(u for u in dataset["users"] if u["userName"] == _USERNAME)
    return user["id"]


@pytest.mark.e2e
@pytest.mark.skip
@allure.feature("Account / Organizations menu (E2E)")
@allure.title("Switch active organization from the account menu")
def test_account_menu_organizations_change(
    global_settings: GlobalSettings,
    page: Page,
) -> None:
    sign_in_page = SignInPage(global_settings=global_settings, page=page)

    with allure.step(f"Sign in as {_USERNAME}"):
        sign_in_page.navigate()
        sign_in_page.email_input.fill(_USERNAME)
        sign_in_page.password_input.fill(global_settings.users_password.get_secret_value())
        sign_in_page.sign_in_button.click()

    home_page = HomePage(global_settings=global_settings, page=page)

    with allure.step(f"Verify current organization is '{_ORIGINAL_ORGANIZATION_NAME}'"):
        expect(home_page.top_header.account_button.customer_name_label).to_be_visible()
        expect(home_page.top_header.account_button.organization_name_label).to_be_visible()
        expect(home_page.top_header.account_button.organization_name_label).to_have_text(_ORIGINAL_ORGANIZATION_NAME)

    with allure.step(f"Switch organization to '{_TARGET_ORGANIZATION_NAME}'"):
        home_page.top_header.account_button.root.click()
        expect(home_page.top_header.account_menu.root).to_be_visible()
        home_page.top_header.account_menu.select_organization(name=_TARGET_ORGANIZATION_NAME)
        expect(home_page.top_header.account_button.organization_name_label).to_have_text(_TARGET_ORGANIZATION_NAME)

    with allure.step(f"Switch back to '{_ORIGINAL_ORGANIZATION_NAME}'"):
        home_page.top_header.account_button.root.click()
        home_page.top_header.account_menu.select_organization(name=_ORIGINAL_ORGANIZATION_NAME)


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_user(_USERNAME)
@allure.feature("Account / Organizations menu (E2E)")
@allure.title("Search organizations by partial name")
def test_account_menu_organizations_search(
    global_settings: GlobalSettings,
    page: Page,
) -> None:
    home_page = HomePage(global_settings=global_settings, page=page)

    with allure.step("Open account menu and reveal organizations search"):
        home_page.navigate()
        home_page.top_header.account_button.root.click()
        expect(home_page.top_header.account_menu.root).to_be_visible()
        expect(home_page.top_header.account_menu.search_organizations_input).to_be_visible()
        expect(home_page.top_header.account_menu.search_organizations_button).to_be_visible()

    part_of_org_name = "ACME Store"
    with allure.step(f"Search organizations by '{part_of_org_name}'"):
        home_page.top_header.account_menu.search_organizations_input.fill(part_of_org_name)
        home_page.top_header.account_menu.search_organizations_button.click()
        expect(home_page.top_header.account_menu.organizations_list.first).to_be_visible()

    with allure.step(f"Verify all returned organizations contain '{part_of_org_name}'"):
        orgs = home_page.top_header.account_menu.organizations_list
        names = [orgs.nth(i).get_attribute("data-organization-name") for i in range(orgs.count())]
        assert len(names) > 1, "No search results found (only the pinned current organization)"
        assert all(
            part_of_org_name.lower() in name.lower() for name in names if name
        ), f"Not all organizations contain '{part_of_org_name}': {names}"


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_user(_USERNAME)
@allure.feature("Account / Organizations menu (E2E)")
@allure.title("Search organizations with no matches shows empty state")
def test_account_menu_organizations_search_not_found(
    global_settings: GlobalSettings,
    page: Page,
) -> None:
    home_page = HomePage(global_settings=global_settings, page=page)

    with allure.step("Open account menu and reveal organizations search"):
        home_page.navigate()
        home_page.top_header.account_button.root.click()
        expect(home_page.top_header.account_menu.root).to_be_visible()
        expect(home_page.top_header.account_menu.search_organizations_input).to_be_visible()
        expect(home_page.top_header.account_menu.search_organizations_button).to_be_visible()

    with allure.step("Search organizations by 'NonExistentOrg' and verify empty list"):
        home_page.top_header.account_menu.search_organizations_input.fill("NonExistentOrg")
        home_page.top_header.account_menu.search_organizations_button.click()
        expect(home_page.top_header.account_menu.orgnanizations_empty_list).to_be_visible()


@pytest.mark.e2e
@pytest.mark.skip
@pytest.mark.with_user(_USERNAME)
@pytest.mark.parametrize("search_term, char_description", _SPECIAL_CHAR_ORG_TEST_DATA)
@allure.feature("Account / Organizations menu (E2E)")
@allure.title("Search organizations with special characters")
def test_account_menu_organizations_search_special_characters(
    global_settings: GlobalSettings,
    page: Page,
    search_term: str,
    char_description: str,
) -> None:
    home_page = HomePage(global_settings=global_settings, page=page)

    with allure.step("Open account menu and reveal organizations search"):
        home_page.navigate()
        home_page.top_header.account_button.root.click()
        expect(home_page.top_header.account_menu.root).to_be_visible()
        expect(home_page.top_header.account_menu.search_organizations_input).to_be_visible()
        expect(home_page.top_header.account_menu.search_organizations_button).to_be_visible()

    with allure.step(f"Search organizations by '{search_term}' ({char_description})"):
        home_page.top_header.account_menu.search_organizations_input.fill(search_term)
        home_page.top_header.account_menu.search_organizations_button.click()

    with allure.step(f"Verify at least one organization matches '{search_term.strip()}'"):
        orgs = home_page.top_header.account_menu.organizations_list
        expect(orgs.first).to_be_visible()
        names = [orgs.nth(i).get_attribute("data-organization-name") for i in range(orgs.count())]
        assert len(names) > 1, "No search results found (only the pinned current organization)"
        assert any(
            search_term.strip().lower() in name.lower() for name in names if name
        ), f"Expected at least one organization to contain '{search_term.strip()}', got {names}"


@pytest.mark.e2e
@pytest.mark.skip
@allure.feature("Account / Organizations menu (E2E)")
@allure.title("VCST-5317 AC-1/AC-2: a locked organization stays in the switcher, disabled")
def test_account_menu_organizations_locked_org_disabled(
    global_settings: GlobalSettings,
    page: Page,
    dataset: dict[str, list[dict[str, Any]]],
    lock_membership: Callable[..., None],
) -> None:
    user_id = _employee_1_user_id(dataset)

    with allure.step(f"Lock {_USERNAME} in {_TARGET_ORGANIZATION_NAME} ({_TARGET_ORGANIZATION_ID})"):
        lock_membership(user_id=user_id, organization_id=_TARGET_ORGANIZATION_ID)

    _sign_in(global_settings, page)

    home_page = HomePage(global_settings=global_settings, page=page)

    with allure.step("Open account menu and reveal organizations list"):
        # The modal can render after _sign_in()'s own dismiss already ran (observed as
        # flaky timing, not tied to which org(s) are locked) — check again before clicking.
        _dismiss_password_expiry_modal(page)
        home_page.top_header.account_button.root.click()
        expect(home_page.top_header.account_menu.root).to_be_visible()

    with allure.step(f"Verify {_TARGET_ORGANIZATION_NAME} is present but disabled (not selectable)"):
        expect(home_page.top_header.account_menu.find_organization(_TARGET_ORGANIZATION_NAME)).to_be_visible()
        expect(home_page.top_header.account_menu.find_organization_option(_TARGET_ORGANIZATION_NAME)).to_be_disabled()

    with allure.step(f"Verify {_ORIGINAL_ORGANIZATION_NAME} (not locked) is present and selectable"):
        expect(home_page.top_header.account_menu.find_organization(_ORIGINAL_ORGANIZATION_NAME)).to_be_visible()
        expect(home_page.top_header.account_menu.find_organization_option(_ORIGINAL_ORGANIZATION_NAME)).to_be_enabled()


@pytest.mark.e2e
@pytest.mark.skip
@allure.feature("Account / Organizations menu (E2E)")
@allure.title("VCST-5317 AC-6: every organization locked disables the whole list, account pages stay reachable")
def test_account_menu_organizations_all_locked_all_disabled(
    global_settings: GlobalSettings,
    page: Page,
    dataset: dict[str, list[dict[str, Any]]],
    lock_membership: Callable[..., None],
) -> None:
    user_id = _employee_1_user_id(dataset)
    organization_ids = _employee_1_organization_ids(dataset)
    assert len(organization_ids) > 1, "Precondition: employee_1 must have more than one seeded organization"

    with allure.step(f"Lock {_USERNAME} in all {len(organization_ids)} seeded organizations"):
        for organization_id in organization_ids:
            lock_membership(user_id=user_id, organization_id=organization_id)

    _sign_in(global_settings, page)

    home_page = HomePage(global_settings=global_settings, page=page)

    with allure.step("Open account menu"):
        # The modal can render after _sign_in()'s own dismiss already ran (observed as
        # flaky timing, not tied to which org(s) are locked) — check again before clicking.
        _dismiss_password_expiry_modal(page)
        home_page.top_header.account_button.root.click()
        expect(home_page.top_header.account_menu.root).to_be_visible()

    with allure.step("Verify the full organizations list is shown, all rows disabled"):
        options = home_page.top_header.account_menu.organizations_options
        expect(options).to_have_count(len(organization_ids))
        for i in range(options.count()):
            expect(options.nth(i)).to_be_disabled()

    with allure.step("Verify account-level pages remain accessible (AC-6)"):
        home_page.top_header.account_menu.dashboard_link.click()
        expect(page).to_have_url(re.compile(r"/account/dashboard"))
