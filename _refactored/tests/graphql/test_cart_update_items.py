import pytest
from core.clients import GraphQLClient
from gql.operations import CartOperations
from gql.types import CartItemInput
from tests.context import Context

from utils.line_item_utils import has_line_item

_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_VARIATION_ID = "smartphone-apple-iphone-17-256gb-mist-blue"
_INITIAL_QUANTITY = 3
_TARGET_QUANTITY = 5


@pytest.mark.graphql
@pytest.mark.delete_cart_after
def test_cart_update_product_items(graphql_client: GraphQLClient, ctx: Context) -> None:
    cart_ops = CartOperations(client=graphql_client)

    cart = cart_ops.update_cart_quantity(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        items=[CartItemInput(product_id=_PRODUCT_ID, quantity=_INITIAL_QUANTITY)],
    )
    assert has_line_item(cart.items, product_id=_PRODUCT_ID, quantity=_INITIAL_QUANTITY)

    cart = cart_ops.update_cart_quantity(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        items=[CartItemInput(product_id=_PRODUCT_ID, quantity=_TARGET_QUANTITY)],
    )
    assert has_line_item(cart.items, product_id=_PRODUCT_ID, quantity=_TARGET_QUANTITY)


@pytest.mark.graphql
@pytest.mark.delete_cart_after
def test_cart_update_variation_items(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    cart_ops = CartOperations(client=graphql_client)

    cart = cart_ops.update_cart_quantity(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        items=[CartItemInput(product_id=_VARIATION_ID, quantity=_INITIAL_QUANTITY)],
    )
    assert has_line_item(
        cart.items, product_id=_VARIATION_ID, quantity=_INITIAL_QUANTITY
    )

    cart = cart_ops.update_cart_quantity(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        items=[CartItemInput(product_id=_VARIATION_ID, quantity=_TARGET_QUANTITY)],
    )
    assert has_line_item(
        cart.items, product_id=_VARIATION_ID, quantity=_TARGET_QUANTITY
    )
