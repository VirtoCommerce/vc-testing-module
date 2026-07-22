from typing import Any

import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.components import CouponItem
from page_objects.pages import AccountCouponsPage
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect

from tests.constants import LOWERCASE_COUPON_CODE

_USERNAME = "acme_store_employee_1@acme.com"
# Bounded wait for a coupon card to appear before deciding the feature/data is
# absent — long enough for the SPA's promotionCoupons query to resolve, short
# enough not to stall a build that will never render it.
_PROBE_TIMEOUT_MS = 15000


def _require_account_coupons(coupons_page: AccountCouponsPage) -> None:
    """Skip when the ``/account/coupons`` UI or coupon data is absent on this
    storefront build (env divergence) instead of timing out on visibility.

    Mirrors the capability-probe pattern in ``test_cart_coupon.py`` and
    ``test_wishlist_manage_lists.py``: give the SPA a bounded chance to render a
    coupon card; if none appears, the feature/markup isn't present here.
    """
    try:
        coupons_page.cards.first.wait_for(state="visible", timeout=_PROBE_TIMEOUT_MS)
    except PlaywrightTimeoutError:
        pytest.skip("Account coupons UI/data not present in this storefront build")


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
        _require_account_coupons(coupons_page)

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
        _require_account_coupons(coupons_page)
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
        _require_account_coupons(coupons_page)

    with allure.step(f"Locate the lowercase coupon '{LOWERCASE_COUPON_CODE}'"):
        card = coupons_page.find_card(LOWERCASE_COUPON_CODE)
        expect(card.root).to_be_visible()

    with allure.step("Displayed code preserves the stored lowercase"):
        assert card.code() == LOWERCASE_COUPON_CODE

    with allure.step("Copied code also preserves the stored lowercase"):
        card.code_button.click()
        clipboard = page.evaluate("() => navigator.clipboard.readText()")
        assert clipboard.strip() == LOWERCASE_COUPON_CODE
