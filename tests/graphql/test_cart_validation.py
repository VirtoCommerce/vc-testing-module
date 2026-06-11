"""Cart validation errors with ruleSet — per-line and cart-level (VCST-5240).

Regression coverage for VCST-5234: after a cart change, an over-stock line must
keep reporting ``isValid: false`` + per-line ``validationErrors`` (these used to
vanish — the line read back valid-when-invalid). Also guards ruleSet scoping and
within-/cross-request ruleSet cache isolation introduced by XCart PR #110.

Repro shape: add a valid line (qty 1), then push it over stock via
``updateCartQuantity``. The over-stock quantity sits above the product's seeded
stock but below the platform's 999_999 per-line cap, so the inventory rule fires
(``PRODUCT_QTY_CHANGED`` / LineItem scope) rather than the line-limit rule.
Carts are anonymous (random ``ctx.user_id``), matching the other cart suites.
"""

import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import CartOperations
from gql.types import CartItemInput
from tests.context import Context

# In-stock, inventory-tracked products in the seeded ACME catalog.
_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_SIBLING_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-sage"
_VALID_QTY = 1
_SIBLING_QTY = 2
# Above the seeded stock (~137k) yet below the 999_999 per-line cap, so the
# over-stock inventory rule fires instead of LINE_ITEM_LIMIT.
_OVER_STOCK_QTY = 500_000

# Per-line / item over-stock surfaces under these codes (LineItem scope).
_QTY_ERROR_CODES = {"PRODUCT_QTY_CHANGED", "PRODUCT_QTY_INSUFFICIENT"}


def _find_line(items: list[dict], product_id: str) -> dict | None:
    return next((i for i in items if i["productId"] == product_id), None)


def _error_codes(errors: list[dict]) -> set[str]:
    return {e["errorCode"] for e in errors}


def _has_qty_error(errors: list[dict]) -> bool:
    return bool(_error_codes(errors) & _QTY_ERROR_CODES)


def _seed_over_stock_line(cart_ops: CartOperations, ctx: Context) -> None:
    """Add a valid line, then push it over stock via an update."""
    cart_ops.add_items_to_cart(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
        items=[CartItemInput(product_id=_PRODUCT_ID, quantity=_VALID_QTY)],
    )
    cart_ops.update_cart_quantity(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
        items=[CartItemInput(product_id=_PRODUCT_ID, quantity=_OVER_STOCK_QTY)],
    )


@pytest.mark.graphql
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("Per-line validationErrors survive an over-stock quantity change")
def test_line_item_validation_survives_overstock_update(graphql_client: GraphQLClient, ctx: Context) -> None:
    """VCST-5234 core guard: an over-stock line reports isValid=false + a
    per-line quantity error. Read per-line only (no cart-level validationErrors
    field) so nothing re-validates the aggregate — the decisive probe."""
    cart_ops = CartOperations(client=graphql_client)

    with allure.step(f"Add {_PRODUCT_ID}×{_VALID_QTY}, then update to {_OVER_STOCK_QTY}"):
        _seed_over_stock_line(cart_ops, ctx)

    with allure.step("Read per-line validation only (no cart-level re-validation)"):
        cart = cart_ops.get_cart_line_validation(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
        )

    with allure.step("Verify the over-stock line is invalid with a quantity error"):
        line = _find_line(cart["items"], _PRODUCT_ID)
        assert line is not None, "over-stock line was not retained in the cart"
        assert line["isValid"] is False
        assert _has_qty_error(
            line["validationErrors"]
        ), f"expected a quantity error, got {_error_codes(line['validationErrors'])}"


@pytest.mark.graphql
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("Per-line validationErrors persist after a subsequent cart change")
def test_line_item_validation_persists_after_subsequent_change(graphql_client: GraphQLClient, ctx: Context) -> None:
    """The literal VCST-5234 symptom: per-line errors must NOT disappear after a
    later cart change. Over-stock a line, then add an unrelated valid line (a
    save), and confirm the over-stock line is still invalid."""
    cart_ops = CartOperations(client=graphql_client)

    with allure.step("Create an over-stock line"):
        _seed_over_stock_line(cart_ops, ctx)

    with allure.step(f"Add a valid sibling line {_SIBLING_PRODUCT_ID}×{_SIBLING_QTY}"):
        cart_ops.add_items_to_cart(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
            items=[CartItemInput(product_id=_SIBLING_PRODUCT_ID, quantity=_SIBLING_QTY)],
        )

    with allure.step("Verify the over-stock line is STILL invalid after the change"):
        cart = cart_ops.get_cart_line_validation(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
        )
        line = _find_line(cart["items"], _PRODUCT_ID)
        assert line is not None and line["isValid"] is False
        assert _has_qty_error(line["validationErrors"])


@pytest.mark.graphql
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("Per-line validity is isolated between lines")
def test_line_item_validation_isolated_across_lines(graphql_client: GraphQLClient, ctx: Context) -> None:
    """An over-stock line must not contaminate a sibling valid line: the
    over-stock line is invalid while the in-stock line stays valid."""
    cart_ops = CartOperations(client=graphql_client)

    with allure.step("Add two valid lines, then push one over stock"):
        cart_ops.add_items_to_cart(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
            items=[
                CartItemInput(product_id=_PRODUCT_ID, quantity=_VALID_QTY),
                CartItemInput(product_id=_SIBLING_PRODUCT_ID, quantity=_SIBLING_QTY),
            ],
        )
        cart_ops.update_cart_quantity(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
            items=[CartItemInput(product_id=_PRODUCT_ID, quantity=_OVER_STOCK_QTY)],
        )

    with allure.step("Verify over-stock line invalid, sibling line valid"):
        cart = cart_ops.get_cart_line_validation(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
        )
        over = _find_line(cart["items"], _PRODUCT_ID)
        sibling = _find_line(cart["items"], _SIBLING_PRODUCT_ID)
        assert over is not None and over["isValid"] is False
        assert _has_qty_error(over["validationErrors"])
        assert sibling is not None and sibling["isValid"] is True
        assert sibling["validationErrors"] == []


@pytest.mark.graphql
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("Cart-level validationErrors are scoped per ruleSet")
def test_cart_validation_ruleset_scoping(graphql_client: GraphQLClient, ctx: Context) -> None:
    """The item over-stock error belongs to the items scope: it surfaces under
    ruleSet ``*`` (union) and ``items``, but not under ``default``/``shipments``,
    and an unknown ruleSet returns nothing. The per-line signal stays invalid
    regardless of which cart-level ruleSet is queried."""
    cart_ops = CartOperations(client=graphql_client)

    with allure.step("Create an over-stock line"):
        _seed_over_stock_line(cart_ops, ctx)

    def read(rule_set: str) -> dict:
        return cart_ops.get_cart_validation(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
            rule_set=rule_set,
        )

    with allure.step("ruleSet '*' and 'items' surface the over-stock error"):
        for rule_set in ("*", "items"):
            cart = read(rule_set)
            assert _has_qty_error(cart["validationErrors"]), f"ruleSet {rule_set!r} should contain the over-stock error"

    with allure.step("ruleSet 'default', 'shipments', 'foo' do NOT carry item-qty errors"):
        for rule_set in ("default", "shipments", "foo"):
            cart = read(rule_set)
            assert not _has_qty_error(
                cart["validationErrors"]
            ), f"ruleSet {rule_set!r} must not contain the item-qty error"
            # per-line validity is independent of the cart-level ruleSet queried
            line = _find_line(cart["items"], _PRODUCT_ID)
            assert line is not None and line["isValid"] is False


@pytest.mark.graphql
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("ruleSet cache is isolated within a single request")
def test_cart_validation_ruleset_isolation_within_request(graphql_client: GraphQLClient, ctx: Context) -> None:
    """Two ruleSet-scoped validationErrors selections in one request (aliases)
    must not leak into or poison each other (VCST-4952 / PR #110)."""
    cart_ops = CartOperations(client=graphql_client)

    with allure.step("Create an over-stock line"):
        _seed_over_stock_line(cart_ops, ctx)

    with allure.step("'*' then 'shipments' in one request: only '*' carries the error"):
        cart = cart_ops.get_cart_validation_aliased(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
            rule_set_a="*",
            rule_set_b="shipments",
        )
        assert _has_qty_error(cart["errorsA"])
        assert not _has_qty_error(cart["errorsB"])

    with allure.step("unknown 'foo' then '*' in one request: 'foo' must not poison '*'"):
        cart = cart_ops.get_cart_validation_aliased(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
            rule_set_a="foo",
            rule_set_b="*",
        )
        assert cart["errorsA"] == []
        assert _has_qty_error(cart["errorsB"])


@pytest.mark.graphql
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("ruleSet cache is isolated across separate requests")
def test_cart_validation_ruleset_isolation_across_requests(graphql_client: GraphQLClient, ctx: Context) -> None:
    """Querying one ruleSet must not leak into / poison a subsequent request's
    ruleSet (each get_cart_validation call is a separate POST)."""
    cart_ops = CartOperations(client=graphql_client)

    with allure.step("Create an over-stock line"):
        _seed_over_stock_line(cart_ops, ctx)

    def read(rule_set: str) -> dict:
        return cart_ops.get_cart_validation(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
            rule_set=rule_set,
        )

    with allure.step("'*' (req 1) carries the error; 'shipments' (req 2) does not"):
        assert _has_qty_error(read("*")["validationErrors"])
        assert not _has_qty_error(read("shipments")["validationErrors"])

    with allure.step("unknown 'foo' (req 1) does not poison '*' (req 2)"):
        assert not _has_qty_error(read("foo")["validationErrors"])
        assert _has_qty_error(read("*")["validationErrors"])


@pytest.mark.graphql
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("Validation errors clear after the cart is corrected")
def test_cart_validation_clears_after_correction(graphql_client: GraphQLClient, ctx: Context) -> None:
    """After correcting the quantity back within stock, both cart-level and
    per-line validation errors must clear (no stale errors)."""
    cart_ops = CartOperations(client=graphql_client)

    with allure.step("Create an over-stock line"):
        _seed_over_stock_line(cart_ops, ctx)

    with allure.step(f"Correct the quantity back to {_VALID_QTY}"):
        cart_ops.update_cart_quantity(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
            items=[CartItemInput(product_id=_PRODUCT_ID, quantity=_VALID_QTY)],
        )

    with allure.step("Verify cart-level and per-line errors are cleared"):
        cart = cart_ops.get_cart_validation(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
            rule_set="*",
        )
        assert not _has_qty_error(cart["validationErrors"])
        line = _find_line(cart["items"], _PRODUCT_ID)
        assert line is not None
        assert line["isValid"] is True
        assert line["validationErrors"] == []
