from decimal import Decimal

import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import CartOperations
from gql.types import Cart
from tests.constants import (
    EXPIRED_COUPON_CODE,
    FIXED_COUPON_AMOUNT,
    FIXED_COUPON_CODE,
    LOWERCASE_COUPON_CODE,
    PERCENTAGE_COUPON_CODE,
    PERCENTAGE_PCT,
    SALE_PRODUCT_ID,
)
from tests.context import Context

_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_QUANTITY = 3
_COUPON_CODE = "COUPON-100-OFF"
_SALE_QUANTITY = 2
_UNKNOWN_COUPON_CODE = "NO-SUCH-COUPON-QA-ZZZ"


def _add_coupon(cart_ops: CartOperations, ctx: Context, code: str) -> Cart:
    return cart_ops.add_coupon(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
        code=code,
    )


def _remove_coupon(cart_ops: CartOperations, ctx: Context, code: str) -> Cart:
    return cart_ops.remove_coupon(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
        code=code,
    )


def _validate_coupon(cart_ops: CartOperations, ctx: Context, cart_id: str, code: str) -> bool:
    return cart_ops.validate_coupon(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        cart_id=cart_id,
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
        coupon=code,
    )


def _assert_totals_consistent(cart: Cart) -> None:
    """BL-CHK-006: subTotal - discountTotal + taxTotal + shipping == grandTotal.

    Holds by construction regardless of how tax is derived, so it is a safe,
    non-brittle invariant to assert after any discount is applied. Assumes
    feeTotal == 0 (no cart-level fees are configured in the test dataset); a
    non-zero fee would need to be added to the right-hand side.
    """
    expected = cart.sub_total.amount - cart.discount_total.amount + cart.tax_total.amount + cart.shipping_total.amount
    assert abs(cart.total.amount - expected) <= Decimal("0.01"), (
        f"Totals inconsistent: subTotal={cart.sub_total.amount} "
        f"discountTotal={cart.discount_total.amount} taxTotal={cart.tax_total.amount} "
        f"shipping={cart.shipping_total.amount} grandTotal={cart.total.amount}"
    )


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (GraphQL)")
@allure.title("Add and remove a coupon on the cart")
def test_cart_coupon(graphql_client: GraphQLClient, ctx: Context) -> None:
    cart_ops = CartOperations(client=graphql_client)

    with allure.step(f"Add coupon {_COUPON_CODE} to cart"):
        cart = _add_coupon(cart_ops, ctx, _COUPON_CODE)

    with allure.step(f"Verify coupon {_COUPON_CODE} is applied successfully"):
        assert cart is not None
        assert cart.coupons is not None and len(cart.coupons) == 1

        coupon = cart.coupons[0]
        assert coupon.code == _COUPON_CODE
        assert coupon.is_applied_successfully == True

    with allure.step(f"Remove coupon {_COUPON_CODE} from cart"):
        cart = _remove_coupon(cart_ops, ctx, _COUPON_CODE)

    with allure.step("Verify cart has no coupons"):
        assert cart is not None
        assert cart.coupons is not None and len(cart.coupons) == 0


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
@allure.feature("Cart / Coupons (GraphQL)")
@allure.title("Validate a valid, an expired, and an unknown coupon")
def test_validate_coupon_valid_and_invalid(graphql_client: GraphQLClient, ctx: Context, with_cart: Cart) -> None:
    cart_ops = CartOperations(client=graphql_client)
    assert with_cart is not None

    with allure.step(f"Valid coupon '{PERCENTAGE_COUPON_CODE}' validates as true"):
        assert _validate_coupon(cart_ops, ctx, with_cart.id, PERCENTAGE_COUPON_CODE) is True

    with allure.step(f"Expired coupon '{EXPIRED_COUPON_CODE}' validates as false"):
        assert _validate_coupon(cart_ops, ctx, with_cart.id, EXPIRED_COUPON_CODE) is False

    with allure.step(f"Unknown coupon '{_UNKNOWN_COUPON_CODE}' validates as false"):
        assert _validate_coupon(cart_ops, ctx, with_cart.id, _UNKNOWN_COUPON_CODE) is False


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (GraphQL)")
@allure.title("Switching the cart coupon keeps only the last applied code")
def test_cart_coupon_single_slot_last_wins(graphql_client: GraphQLClient, ctx: Context) -> None:
    # The storefront treats the cart coupon as a single slot: to switch codes it
    # removes the current one and adds the next. This test drives that flow and
    # asserts the cart ends with exactly the last-applied coupon.
    cart_ops = CartOperations(client=graphql_client)

    with allure.step(f"Apply first coupon '{_COUPON_CODE}'"):
        cart = _add_coupon(cart_ops, ctx, _COUPON_CODE)
        assert any(c.code == _COUPON_CODE and c.is_applied_successfully for c in cart.coupons)

    with allure.step(f"Switch to '{PERCENTAGE_COUPON_CODE}' (remove then add)"):
        _remove_coupon(cart_ops, ctx, _COUPON_CODE)
        cart = _add_coupon(cart_ops, ctx, PERCENTAGE_COUPON_CODE)

    with allure.step("Only the last coupon remains and is applied"):
        assert [c.code for c in cart.coupons] == [PERCENTAGE_COUPON_CODE]
        assert all(c.is_applied_successfully for c in cart.coupons)
        assert cart.discount_total.amount > 0
        _assert_totals_consistent(cart)


@pytest.mark.graphql
@pytest.mark.with_cart([(SALE_PRODUCT_ID, _SALE_QUANTITY)])
@allure.feature("Cart / Coupons (GraphQL)")
@allure.title("Percentage coupon discounts the sale price, not the list price")
def test_cart_coupon_percentage_on_sale_price(graphql_client: GraphQLClient, ctx: Context, with_cart: Cart) -> None:
    cart_ops = CartOperations(client=graphql_client)
    assert with_cart is not None

    line = next(i for i in with_cart.items if i.product_id == SALE_PRODUCT_ID)
    assert line.sale_price is not None and line.list_price is not None
    sale_unit = line.sale_price.amount
    list_unit = line.list_price.amount

    with allure.step("Seeded line item is on sale (sale price below list price)"):
        assert sale_unit < list_unit

    baseline_discount = with_cart.discount_total.amount

    with allure.step(f"Apply percentage coupon '{PERCENTAGE_COUPON_CODE}'"):
        cart = _add_coupon(cart_ops, ctx, PERCENTAGE_COUPON_CODE)
        assert any(c.code == PERCENTAGE_COUPON_CODE and c.is_applied_successfully for c in cart.coupons)

    applied_line = next(i for i in cart.items if i.product_id == SALE_PRODUCT_ID)
    coupon_discount = cart.discount_total.amount - baseline_discount
    pct = Decimal(PERCENTAGE_PCT) / Decimal(100)
    expected_on_sale = (sale_unit * applied_line.quantity * pct).quantize(Decimal("0.01"))
    expected_on_list = (list_unit * applied_line.quantity * pct).quantize(Decimal("0.01"))

    with allure.step("Coupon discount equals the percentage of the SALE price"):
        assert abs(coupon_discount - expected_on_sale) <= Decimal(
            "0.02"
        ), f"coupon_discount={coupon_discount} expected_on_sale={expected_on_sale}"

    with allure.step("Coupon discount is strictly less than the list-price basis"):
        assert coupon_discount < expected_on_list

    with allure.step("Cart totals remain consistent (BL-CHK-006)"):
        _assert_totals_consistent(cart)


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (GraphQL)")
@allure.title("Applying an expired or unknown coupon adds it unapplied with no discount")
def test_cart_coupon_expired_and_unknown_not_applied(
    graphql_client: GraphQLClient, ctx: Context, with_cart: Cart
) -> None:
    # User-facing negative path: addCoupon accepts any code string, but an
    # expired/unknown code must resolve as not-applied and produce no discount.
    cart_ops = CartOperations(client=graphql_client)
    assert with_cart is not None
    baseline_discount = with_cart.discount_total.amount

    for code in (EXPIRED_COUPON_CODE, _UNKNOWN_COUPON_CODE):
        with allure.step(f"Apply invalid coupon '{code}'"):
            cart = _add_coupon(cart_ops, ctx, code)
        with allure.step(f"'{code}' is present but not applied, and adds no discount"):
            applied = next((c for c in cart.coupons if c.code.upper() == code.upper()), None)
            assert applied is not None, f"Coupon '{code}' was not recorded on the cart"
            assert applied.is_applied_successfully is False
            assert cart.discount_total.amount == baseline_discount


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (GraphQL)")
@allure.title("Fixed-amount coupon discounts the cart by its absolute value")
def test_cart_coupon_fixed_amount(graphql_client: GraphQLClient, ctx: Context, with_cart: Cart) -> None:
    cart_ops = CartOperations(client=graphql_client)
    assert with_cart is not None
    baseline_discount = with_cart.discount_total.amount
    fixed_amount = Decimal(FIXED_COUPON_AMOUNT)

    # The seeded cart subtotal must exceed the fixed amount for the full $20 to
    # apply (absolute cart rewards are capped at the cart total).
    assert with_cart.sub_total.amount > fixed_amount

    with allure.step(f"Apply fixed-amount coupon '{FIXED_COUPON_CODE}'"):
        cart = _add_coupon(cart_ops, ctx, FIXED_COUPON_CODE)
        assert any(c.code == FIXED_COUPON_CODE and c.is_applied_successfully for c in cart.coupons)

    with allure.step("Discount equals the coupon's absolute amount"):
        coupon_discount = cart.discount_total.amount - baseline_discount
        assert abs(coupon_discount - fixed_amount) <= Decimal(
            "0.01"
        ), f"coupon_discount={coupon_discount} expected={fixed_amount}"

    with allure.step("Cart totals remain consistent (BL-CHK-006)"):
        _assert_totals_consistent(cart)


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (GraphQL)")
@allure.title("Lowercase coupon applied via any input case preserves its stored case")
def test_cart_coupon_lowercase_code_roundtrip(graphql_client: GraphQLClient, ctx: Context) -> None:
    # VCST-5233 data-layer guard: the coupon is stored lowercase. Applying the
    # exact lowercase code must round-trip verbatim (not be upper-cased), and an
    # upper-cased input must still match case-insensitively and apply.
    cart_ops = CartOperations(client=graphql_client)

    with allure.step(f"Apply the exact lowercase code '{LOWERCASE_COUPON_CODE}'"):
        cart = _add_coupon(cart_ops, ctx, LOWERCASE_COUPON_CODE)
        applied = next((c for c in cart.coupons if c.code.lower() == LOWERCASE_COUPON_CODE), None)
        assert applied is not None
        assert applied.is_applied_successfully is True
        assert applied.code == LOWERCASE_COUPON_CODE, f"Stored code was not preserved lowercase: {applied.code!r}"

    with allure.step("Re-apply with an upper-cased input; matching is case-insensitive"):
        _remove_coupon(cart_ops, ctx, LOWERCASE_COUPON_CODE)
        cart = _add_coupon(cart_ops, ctx, LOWERCASE_COUPON_CODE.upper())
        applied = next((c for c in cart.coupons if c.code.lower() == LOWERCASE_COUPON_CODE), None)
        assert applied is not None
        assert applied.is_applied_successfully is True
