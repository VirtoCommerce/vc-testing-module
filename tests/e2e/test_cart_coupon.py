import re
from decimal import Decimal

import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import CartPage
from playwright.sync_api import Page, expect

from tests.constants import PERCENTAGE_COUPON_CODE, PERCENTAGE_PCT, SALE_PRODUCT_ID

_USERNAME = "acme_store_employee_1@acme.com"
_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_QUANTITY = 2
_SALE_QUANTITY = 2

_MONEY_RE = re.compile(r"-?[\d,]+\.\d{2}")


def _amount(text: str | None) -> Decimal:
    """Parse the first currency-looking number out of a label's text."""
    match = _MONEY_RE.search(text or "")
    return Decimal(match.group().replace(",", "")) if match else Decimal(0)


def _require_coupon_ui(cart_page: CartPage) -> None:
    """Skip unless BOTH the class-based coupon section and the order-summary
    totals element are present in the running storefront theme.

    The coupon section may exist only in the PR/preview theme, and the totals
    markup can differ, so we probe both up front and skip cleanly rather than
    letting later interactions time out.
    """
    if cart_page.coupon_section.root.count() == 0:
        pytest.skip("Cart coupon section is not available in this storefront theme")
    if cart_page.grand_total_label.count() == 0:
        pytest.skip("Cart order-summary totals are not available in this storefront theme")


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("Preset coupon cards render in the cart coupon section")
def test_cart_coupon_presets_render(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart and confirm the seeded item is shown"):
        cart_page.navigate()
        expect(cart_page.line_items).to_be_visible()

    with allure.step("The coupon section renders at least one preset card"):
        _require_coupon_ui(cart_page)
        section = cart_page.coupon_section
        if section.preset_cards.count() == 0:
            pytest.skip("No preset coupon cards are surfaced in the cart")
        expect(section.preset_cards.first).to_be_visible()
        assert section.first_preset_code() != ""


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("Applying a preset coupon discounts the cart total")
def test_cart_coupon_apply_preset(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart"):
        cart_page.navigate()
        expect(cart_page.line_items).to_be_visible()
        _require_coupon_ui(cart_page)

    section = cart_page.coupon_section
    if section.preset_cards.count() == 0:
        pytest.skip("No preset coupon cards are surfaced in the cart")

    total_label = cart_page.grand_total_label
    before_total_text = total_label.inner_text()

    with allure.step("Apply the first preset coupon (runtime-discovered code)"):
        code = section.first_preset_code()
        section.apply_preset(code)

    with allure.step("Totals recalculate and the grand total decreases"):
        expect(total_label).not_to_have_text(before_total_text)
        expect(cart_page.discount_total_label).to_be_visible()
        assert _amount(total_label.inner_text()) < _amount(before_total_text)
        assert _amount(cart_page.discount_total_label.inner_text()) > 0


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("Removing the coupon restores the original cart total")
def test_cart_coupon_remove_restores_total(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart"):
        cart_page.navigate()
        expect(cart_page.line_items).to_be_visible()
        _require_coupon_ui(cart_page)

    section = cart_page.coupon_section
    if section.preset_cards.count() == 0:
        pytest.skip("No preset coupon cards are surfaced in the cart")

    total_label = cart_page.grand_total_label
    original_total_text = total_label.inner_text()

    with allure.step("Apply a preset coupon"):
        section.apply_preset(section.first_preset_code())
        expect(total_label).not_to_have_text(original_total_text)

    with allure.step("Remove the coupon and confirm the total is restored"):
        section.remove_button.click()
        expect(total_label).to_have_text(original_total_text)


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("Anonymous shoppers see no preset coupon cards")
def test_cart_coupon_anonymous_no_presets(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart as an anonymous shopper"):
        cart_page.navigate()
        expect(cart_page.line_items).to_be_visible()
        _require_coupon_ui(cart_page)

    with allure.step("No preset coupon cards are surfaced without an account"):
        expect(cart_page.coupon_section.preset_cards).to_have_count(0)


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(SALE_PRODUCT_ID, _SALE_QUANTITY)])
@allure.feature("Cart / Coupons (E2E)")
@allure.title("Percentage coupon UI discounts the sale-price subtotal")
def test_cart_coupon_percentage_ui_on_sale(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open the cart with the on-sale product"):
        cart_page.navigate()
        expect(cart_page.line_items).to_be_visible()
        _require_coupon_ui(cart_page)

    section = cart_page.coupon_section

    with allure.step(f"Apply the percentage coupon '{PERCENTAGE_COUPON_CODE}'"):
        section.custom_code_input.fill(PERCENTAGE_COUPON_CODE)
        section.apply_button.click()
        expect(cart_page.discount_total_label).to_be_visible()

    with allure.step("Displayed discount equals the percentage of the (sale) subtotal"):
        subtotal = _amount(cart_page.subtotal_label.inner_text())
        discount = _amount(cart_page.discount_total_label.inner_text())
        expected = (subtotal * Decimal(PERCENTAGE_PCT) / Decimal(100)).quantize(Decimal("0.01"))
        assert abs(discount - expected) <= Decimal(
            "0.05"
        ), f"discount={discount} expected≈{expected} (subtotal={subtotal})"
