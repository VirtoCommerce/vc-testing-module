import re
from decimal import Decimal

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


def _amount(text: str | None) -> Decimal:
    """Parse the first currency-looking number out of a label's text."""
    match = _MONEY_RE.search(text or "")
    return Decimal(match.group().replace(",", "")) if match else Decimal(0)


def _require_coupon_ui(cart_page: CartPage) -> None:
    """Skip when the coupon section isn't present in the running storefront
    build (CI/preview theme divergence) rather than timing out later."""
    if cart_page.coupon_section.root.count() == 0:
        pytest.skip("Cart coupon section is not available in this storefront theme")
    if cart_page.grand_total_label.count() == 0:
        pytest.skip("Cart order-summary totals are not available in this storefront theme")


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("Anonymous shopper sees only the custom-code field and can apply a coupon there")
def test_cart_coupon_anonymous_custom_code(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart as an anonymous shopper"):
        cart_page.navigate()
        expect(cart_page.line_items).to_be_visible()
        _require_coupon_ui(cart_page)

    section = cart_page.coupon_section
    total_label = cart_page.grand_total_label
    before_total_text = total_label.inner_text()

    with allure.step("Only the custom-code field is shown — no presets, no view-all link"):
        expect(section.custom_code_input).to_be_visible()
        expect(section.preset_cards).to_have_count(0)
        expect(section.view_all_link).to_have_count(0)

    with allure.step(f"Apply '{LOWERCASE_COUPON_CODE}' via the custom-code field"):
        section.custom_code_input.fill(LOWERCASE_COUPON_CODE)
        section.apply_button.click()

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
        cart_page.navigate()
        expect(cart_page.line_items).to_be_visible()
        _require_coupon_ui(cart_page)

    section = cart_page.coupon_section
    if section.preset_cards.count() == 0:
        pytest.skip("No public preset coupons are surfaced in the cart")

    with allure.step("The first preset card shows a label, a name, and an apply code"):
        first = section.preset_cards.first
        expect(first).to_be_visible()
        assert first.locator(".coupon-card__label").inner_text().strip() != ""
        assert first.locator(".coupon-card__name").inner_text().strip() != ""
        assert section.first_preset_code() != ""


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("Clicking a preset validates the coupon (green check); clicking another switches it")
def test_cart_coupon_preset_apply_and_switch(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart"):
        cart_page.navigate()
        expect(cart_page.line_items).to_be_visible()
        _require_coupon_ui(cart_page)

    section = cart_page.coupon_section
    if section.preset_cards.count() < 2:
        pytest.skip("Need at least two preset coupons to test switching")

    total_label = cart_page.grand_total_label
    before_total_text = total_label.inner_text()
    percentage_card = section.card_by_name("QA 10% Off Subtotal")
    welcome_card = section.card_by_name("Welcome Offer")

    with allure.step(f"Click the '{PERCENTAGE_COUPON_CODE}' preset — the coupon validates true"):
        section.apply_preset(PERCENTAGE_COUPON_CODE)
        expect(percentage_card).to_have_class(re.compile("coupon-card--applied"))
        expect(section.applied_check_icon).to_be_visible()
        expect(section.applied_cards).to_have_count(1)
        expect(total_label).not_to_have_text(before_total_text)
        assert _amount(total_label.inner_text()) < _amount(before_total_text)

    after_percentage_text = total_label.inner_text()

    with allure.step(f"Click the '{FIXED_COUPON_CODE}' preset — the applied coupon switches to it"):
        section.apply_preset(FIXED_COUPON_CODE)
        expect(welcome_card).to_have_class(re.compile("coupon-card--applied"))
        expect(section.applied_check_icon).to_be_visible()
        expect(percentage_card).not_to_have_class(re.compile("coupon-card--applied"))
        expect(section.applied_cards).to_have_count(1)
        expect(total_label).not_to_have_text(after_percentage_text)


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("Removing an applied custom-code coupon restores the cart")
def test_cart_coupon_remove_restores_cart(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart"):
        cart_page.navigate()
        expect(cart_page.line_items).to_be_visible()
        _require_coupon_ui(cart_page)

    section = cart_page.coupon_section
    total_label = cart_page.grand_total_label
    before_total_text = total_label.inner_text()

    with allure.step(f"Apply '{LOWERCASE_COUPON_CODE}' via the custom-code field"):
        section.custom_code_input.fill(LOWERCASE_COUPON_CODE)
        section.apply_button.click()
        expect(section.remove_button).to_be_visible()

    with allure.step("Remove the coupon and confirm entry state and total are restored"):
        section.remove_button.click()
        expect(section.remove_button).to_be_hidden()
        expect(section.apply_button).to_be_visible()
        expect(total_label).to_have_text(before_total_text)


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("An invalid custom code shows an error and does not discount the cart")
def test_cart_coupon_invalid_code_shows_error(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart"):
        cart_page.navigate()
        expect(cart_page.line_items).to_be_visible()
        _require_coupon_ui(cart_page)

    section = cart_page.coupon_section
    before_total_text = cart_page.grand_total_label.inner_text()

    with allure.step(f"Enter the invalid code '{_INVALID_CODE}' and apply"):
        section.custom_code_input.fill(_INVALID_CODE)
        section.apply_button.click()

    with allure.step("An inline error is shown and the grand total is unchanged"):
        expect(section.error_message).to_be_visible()
        expect(section.error_message).to_contain_text(re.compile("not valid", re.IGNORECASE))
        expect(cart_page.grand_total_label).to_have_text(before_total_text)


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("An expired coupon code is rejected and does not discount the cart")
def test_cart_coupon_expired_code_rejected(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart"):
        cart_page.navigate()
        expect(cart_page.line_items).to_be_visible()
        _require_coupon_ui(cart_page)

    section = cart_page.coupon_section
    before_total_text = cart_page.grand_total_label.inner_text()

    with allure.step(f"Enter the expired code '{EXPIRED_COUPON_CODE}' and apply"):
        section.custom_code_input.fill(EXPIRED_COUPON_CODE)
        section.apply_button.click()

    with allure.step("The expired code is rejected and the grand total is unchanged"):
        expect(section.error_message).to_be_visible()
        expect(cart_page.grand_total_label).to_have_text(before_total_text)
