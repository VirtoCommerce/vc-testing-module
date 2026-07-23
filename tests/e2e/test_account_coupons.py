from typing import Any

import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.components import CouponItem
from page_objects.pages import AccountCouponsPage
from playwright.sync_api import Page, expect

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
        # The copy handler writes via the async Clipboard API, which may not have
        # resolved the instant the click returns; poll briefly for the write.
        clipboard = ""
        for _ in range(10):
            clipboard = page.evaluate("() => navigator.clipboard.readText()").strip()
            if clipboard:
                break
            page.wait_for_timeout(200)
        assert clipboard != "", "Clipboard was empty after clicking the copy button"
        assert clipboard == displayed.strip()
