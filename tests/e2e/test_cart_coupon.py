import re
from decimal import Decimal
from typing import Callable

import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import CartPage
from playwright.sync_api import Page, expect

from tests.constants import (
    EXPIRED_COUPON_CODE,
    FIXED_COUPON_CODE,
    LOWERCASE_COUPON_CODE,
    PERCENTAGE_COUPON_CODE,
)

_USERNAME = "acme_store_employee_1@acme.com"
_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_QUANTITY = 2
_INVALID_CODE = "NOPE-INVALID-123"

_MONEY_RE = re.compile(r"-?[\d,]+\.\d{2}")
_NON_EMPTY = re.compile(r"\S")


def _amount(text: str | None) -> Decimal:
    """Parse the first currency-looking number out of a label's text."""
    match = _MONEY_RE.search(text or "")
    return Decimal(match.group().replace(",", "")) if match else Decimal(0)


def _open_cart(cart_page: CartPage, page: Page) -> None:
    """Open the cart and wait for it to fully settle before asserting.

    The cart is a single-page checkout: on a fresh cart it auto-initializes
    shipment then payment (AddOrUpdateCartShipment -> AddOrUpdateCartPayment),
    a cascade that keeps re-rendering the coupon section for several seconds
    after the load event. Reading during that window is what made the preset
    and coupon assertions flake on faster machines. Waiting for the network to
    go idle lets the whole cascade quiesce, so assertions read a stable cart.
    """
    cart_page.navigate()
    expect(cart_page.line_items).to_be_visible()
    page.wait_for_load_state("networkidle")


def _apply_and_settle(cart_page: CartPage, page: Page, action: Callable[[], None], field: str = "addCoupon") -> None:
    """Trigger a coupon mutation, wait for it to commit, then reopen the settled cart.

    Awaiting the mutation's own GraphQL response guarantees it committed
    server-side before the reopen (so the reload can't cancel the in-flight
    request), and reopening reads the authoritative cart: once the coupon is
    persisted and the promotion re-evaluated, a fresh load's GetFullCart returns
    the final state and shipment/payment are already initialized, so they do not
    re-fire to clobber it. This is what a single post-click assertion could not
    guarantee, because a concurrent background write could land stale last.
    """
    with page.expect_response(
        lambda r: "/graphql" in r.url and r.request.method == "POST" and field in (r.request.post_data or "")
    ):
        action()
    _open_cart(cart_page, page)


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("Anonymous shopper sees only the custom-code field and can apply a coupon there")
def test_cart_coupon_anonymous_custom_code(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart as an anonymous shopper"):
        _open_cart(cart_page, page)

    section = cart_page.coupon_section
    total_label = cart_page.grand_total_label
    before_total_text = total_label.inner_text()

    with allure.step("Only the custom-code field is shown — no presets, no view-all link"):
        expect(section.custom_code_input).to_be_visible()
        expect(section.preset_cards).to_have_count(0)
        expect(section.view_all_link).to_have_count(0)

    with allure.step(f"Apply '{LOWERCASE_COUPON_CODE}' via the custom-code field"):
        section.custom_code_input.fill(LOWERCASE_COUPON_CODE)
        _apply_and_settle(cart_page, page, section.apply_button.click)

    with allure.step("The coupon validates true and the grand total decreases"):
        expect(section.remove_button).to_be_visible()
        expect(total_label).not_to_have_text(before_total_text)
        assert _amount(total_label.inner_text()) < _amount(before_total_text)


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("Preset coupon cards render with a localized label and promotion name")
def test_cart_coupon_presets_render(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart and confirm the seeded item is shown"):
        _open_cart(cart_page, page)

    section = cart_page.coupon_section

    with allure.step("The first preset card shows a label, a name, and an apply code"):
        first = section.preset_cards.first
        expect(first).to_be_visible()
        expect(first.locator(".coupon-card__label")).to_have_text(_NON_EMPTY)
        expect(first.locator(".coupon-card__name")).to_have_text(_NON_EMPTY)
        assert section.first_preset_code() != ""


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("Clicking a preset validates the coupon (green check); clicking another switches it")
def test_cart_coupon_preset_apply_and_switch(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart"):
        _open_cart(cart_page, page)

    section = cart_page.coupon_section
    total_label = cart_page.grand_total_label
    before_total_text = total_label.inner_text()

    with allure.step(f"Click the '{PERCENTAGE_COUPON_CODE}' preset — the coupon validates true"):
        _apply_and_settle(cart_page, page, lambda: section.apply_preset(PERCENTAGE_COUPON_CODE))
        expect(section.applied_check_icon).to_be_visible()
        expect(section.applied_cards).to_have_count(1)
        expect(section.applied_code_input).to_have_value(PERCENTAGE_COUPON_CODE)
        expect(total_label).not_to_have_text(before_total_text)
        assert _amount(total_label.inner_text()) < _amount(before_total_text)

    with allure.step(f"Click the '{FIXED_COUPON_CODE}' preset — the applied coupon switches to it"):
        _apply_and_settle(cart_page, page, lambda: section.apply_preset(FIXED_COUPON_CODE))
        expect(section.applied_check_icon).to_be_visible()
        # Exactly one applied card, now carrying the fixed coupon's code —
        # inherently proves the percentage coupon is no longer applied.
        expect(section.applied_cards).to_have_count(1)
        expect(section.applied_code_input).to_have_value(FIXED_COUPON_CODE)


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("Removing an applied preset coupon restores the cart")
def test_cart_coupon_preset_remove_restores_cart(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart"):
        _open_cart(cart_page, page)

    section = cart_page.coupon_section
    total_label = cart_page.grand_total_label
    before_total_text = total_label.inner_text()

    with allure.step(f"Apply the '{PERCENTAGE_COUPON_CODE}' preset and confirm it is applied"):
        _apply_and_settle(cart_page, page, lambda: section.apply_preset(PERCENTAGE_COUPON_CODE))
        expect(section.applied_check_icon).to_be_visible()
        expect(section.applied_cards).to_have_count(1)
        expect(section.applied_code_input).to_have_value(PERCENTAGE_COUPON_CODE)
        expect(total_label).not_to_have_text(before_total_text)
        assert _amount(total_label.inner_text()) < _amount(before_total_text)

    with allure.step("Remove the preset and confirm the applied state and total are restored"):
        _apply_and_settle(cart_page, page, section.remove_button.click, field="removeCoupon")
        expect(section.applied_cards).to_have_count(0)
        expect(total_label).to_have_text(before_total_text)


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("The 'View all' link navigates to the account coupons page")
def test_cart_coupon_view_all_navigates(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart"):
        _open_cart(cart_page, page)

    section = cart_page.coupon_section

    with allure.step("The link points at the account coupons page"):
        link = section.view_all_link.first
        expect(link).to_be_visible()
        assert (link.get_attribute("href") or "").endswith("/account/coupons")

    # The link opens in a new tab (target="_blank"), so capture the popup page
    # rather than expecting the cart tab itself to navigate.
    with allure.step("Clicking it opens the account coupons page in a new tab"):
        with page.context.expect_page() as new_page_info:
            link.click()
        new_page = new_page_info.value
        new_page.wait_for_load_state("load")
        expect(new_page).to_have_url(re.compile(r"/account/coupons"))


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("Removing an applied custom-code coupon restores the cart")
def test_cart_coupon_remove_restores_cart(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart"):
        _open_cart(cart_page, page)

    section = cart_page.coupon_section
    total_label = cart_page.grand_total_label
    before_total_text = total_label.inner_text()

    with allure.step(f"Apply '{LOWERCASE_COUPON_CODE}' via the custom-code field"):
        section.custom_code_input.fill(LOWERCASE_COUPON_CODE)
        _apply_and_settle(cart_page, page, section.apply_button.click)
        expect(section.remove_button).to_be_visible()

    with allure.step("Remove the coupon and confirm entry state and total are restored"):
        _apply_and_settle(cart_page, page, section.remove_button.click, field="removeCoupon")
        expect(section.remove_button).to_be_hidden()
        expect(section.apply_button).to_be_visible()
        expect(total_label).to_have_text(before_total_text)


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.parametrize(
    "code, case",
    [
        pytest.param(_INVALID_CODE, "unknown", id="unknown"),
        pytest.param(EXPIRED_COUPON_CODE, "expired", id="expired"),
    ],
)
@allure.feature("Cart / Coupons (E2E)")
@allure.title("A rejected coupon code ({case}) shows an error and does not discount the cart")
def test_cart_coupon_bad_code_rejected(page: Page, global_settings: GlobalSettings, code: str, case: str) -> None:
    # Both an unknown code and a found-but-expired code are rejected identically
    # at the UI ("This code is not valid"); the semantic difference between them
    # is covered at the API layer by test_validate_coupon_valid_and_invalid.
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart"):
        _open_cart(cart_page, page)

    section = cart_page.coupon_section
    before_total_text = cart_page.grand_total_label.inner_text()

    with allure.step(f"Enter the {case} code '{code}' and apply"):
        section.custom_code_input.fill(code)
        section.apply_button.click()

    with allure.step("An inline 'not valid' error is shown and the grand total is unchanged"):
        expect(section.error_message).to_be_visible()
        expect(section.error_message).to_contain_text(re.compile("not valid", re.IGNORECASE))
        expect(cart_page.grand_total_label).to_have_text(before_total_text)
