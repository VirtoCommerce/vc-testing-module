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


def _assert_scoped_to_line(line: dict) -> None:

    errors = line["validationErrors"]
    has_object_type = any(e.get("objectType") for e in errors)
    has_object_id = any(e.get("objectId") for e in errors)
    if not (has_object_type or has_object_id):
        # Make the skipped check visible so a green run does not read as if
        # linkage was asserted when the backend returned no scoping metadata.
        with allure.step("scoping metadata absent (no objectType/objectId) — line linkage not asserted"):
            pass
        return
    linked = any(
        ("lineitem" in (e.get("objectType") or "").lower()) or (e.get("objectId") == line["id"]) for e in errors
    )
    assert linked, (
        "expected a per-line validation error scoped to the LineItem "
        f"(objectType ~ LineItem or objectId == {line['id']!r}), got "
        f"{[(e.get('objectType'), e.get('objectId')) for e in errors]}"
    )


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
@pytest.mark.optional
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("Over-stock line should stay invalid with a per-line quantity error")
def test_line_item_validation_survives_overstock_update(graphql_client: GraphQLClient, ctx: Context) -> None:

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
        _assert_scoped_to_line(line)


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("Per-line errors should persist after a subsequent cart change")
def test_line_item_validation_persists_after_subsequent_change(graphql_client: GraphQLClient, ctx: Context) -> None:

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
        _assert_scoped_to_line(line)


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("Valid sibling line should stay valid next to an over-stock line")
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
        _assert_scoped_to_line(over)
        assert sibling is not None and sibling["isValid"] is True
        assert sibling["validationErrors"] == []


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("Cart should expose validationErrors scoped per ruleSet")
def test_cart_validation_ruleset_scoping(graphql_client: GraphQLClient, ctx: Context) -> None:

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
@pytest.mark.optional
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("ruleSet cache should stay isolated within a single request")
def test_cart_validation_ruleset_isolation_within_request(graphql_client: GraphQLClient, ctx: Context) -> None:

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
@pytest.mark.optional
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("ruleSet cache should stay isolated across separate requests")
def test_cart_validation_ruleset_isolation_across_requests(graphql_client: GraphQLClient, ctx: Context) -> None:

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
@pytest.mark.optional
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("Validation errors should clear after the cart is corrected")
def test_cart_validation_clears_after_correction(graphql_client: GraphQLClient, ctx: Context) -> None:

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


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.delete_cart_after
@allure.feature("Cart / Validation (GraphQL)")
@allure.title("Validation errors should clear after the over-stock line is removed")
def test_cart_validation_clears_after_line_removal(graphql_client: GraphQLClient, ctx: Context) -> None:

    cart_ops = CartOperations(client=graphql_client)

    with allure.step("Create an over-stock line"):
        _seed_over_stock_line(cart_ops, ctx)

    with allure.step("Verify the over-stock line is invalid with a per-line error"):
        cart = cart_ops.get_cart_line_validation(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
        )
        line = _find_line(cart["items"], _PRODUCT_ID)
        assert line is not None and line["isValid"] is False
        assert _has_qty_error(line["validationErrors"])
        _assert_scoped_to_line(line)
        line_item_id = line["id"]

    with allure.step("Remove the over-stock line from the cart"):
        cart_ops.remove_cart_item(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            line_item_id=line_item_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
        )

    with allure.step("Verify cart-level and per-line errors for that line are gone"):
        cart = cart_ops.get_cart_validation(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
            rule_set="*",
        )
        assert not _has_qty_error(cart["validationErrors"])
        assert _find_line(cart["items"], _PRODUCT_ID) is None
