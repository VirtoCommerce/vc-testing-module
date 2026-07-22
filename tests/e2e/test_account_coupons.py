from typing import Any

import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.components import CouponItem
from page_objects.pages import AccountCouponsPage
from playwright.sync_api import Page, expect

from tests.constants import LOWERCASE_COUPON_CODE

_USERNAME = "acme_store_employee_1@acme.com"


@pytest.fixture
def browser_context_args(browser_context_args: dict[Any, Any]) -> dict[Any, Any]:
    """Grant clipboard access so copy-to-clipboard assertions can read it back."""
    return {**browser_context_args, "permissions": ["clipboard-read", "clipboard-write"]}


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@allure.feature("Account / Coupons (E2E)")
@allure.title("Account coupons page lists available coupons")
def test_account_coupons_list_renders(page: Page, global_settings: GlobalSettings) -> None:
    coupons_page = AccountCouponsPage(global_settings=global_settings, page=page)

    with allure.step("Open the account coupons page"):
        coupons_page.navigate()

    with allure.step("At least one coupon card is rendered"):
        expect(coupons_page.cards.first).to_be_visible()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@allure.feature("Account / Coupons (E2E)")
@allure.title("Clicking a coupon card copies its code to the clipboard")
def test_account_coupon_copy_to_clipboard(page: Page, global_settings: GlobalSettings) -> None:
    coupons_page = AccountCouponsPage(global_settings=global_settings, page=page)

    with allure.step("Open the account coupons page"):
        coupons_page.navigate()
        expect(coupons_page.cards.first).to_be_visible()

    card = CouponItem(root=coupons_page.cards.first)
    displayed = card.code()

    with allure.step("Click the coupon code button to copy it"):
        card.code_button.click()

    with allure.step("Clipboard contents match the displayed code"):
        clipboard = page.evaluate("() => navigator.clipboard.readText()")
        assert clipboard.strip() != ""
        assert clipboard.strip() == displayed.strip()


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@allure.feature("Account / Coupons (E2E)")
@allure.title("Coupon code preserves its stored lowercase in display and clipboard")
def test_account_coupon_code_case_fidelity(page: Page, global_settings: GlobalSettings) -> None:
    # Regression guard for VCST-5233 (FIXED): a coupon stored in lowercase must
    # be shown and copied verbatim in lowercase — not upper-cased by the UI.
    coupons_page = AccountCouponsPage(global_settings=global_settings, page=page)

    with allure.step("Open the account coupons page"):
        coupons_page.navigate()

    with allure.step(f"Locate the lowercase coupon '{LOWERCASE_COUPON_CODE}'"):
        card = coupons_page.find_card(LOWERCASE_COUPON_CODE)
        expect(card.root).to_be_visible()

    with allure.step("Displayed code preserves the stored lowercase"):
        assert card.code() == LOWERCASE_COUPON_CODE

    with allure.step("Copied code also preserves the stored lowercase"):
        card.code_button.click()
        clipboard = page.evaluate("() => navigator.clipboard.readText()")
        assert clipboard.strip() == LOWERCASE_COUPON_CODE
