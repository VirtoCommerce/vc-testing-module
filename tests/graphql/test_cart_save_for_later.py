import pytest
from core.clients import GraphQLClient
from gql.operations import SaveForLaterOperations
from gql.types.cart import Cart
from tests.context import Context

_USER = "acme_store_maintainer_1@acme.com"
_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"


@pytest.mark.graphql
@pytest.mark.with_user(_USER)
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
def test_cart_save_for_later(graphql_client: GraphQLClient, ctx: Context, with_cart: Cart) -> None:
    sfl_ops = SaveForLaterOperations(client=graphql_client)
    cart = with_cart

    assert len(cart.items) == 1
    line_item_id = cart.items[0].id

    result = sfl_ops.move_to_saved_for_later(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        cart_id=cart.id,
        line_item_ids=[line_item_id],
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
    )
    assert result.cart.items_count == 0
    assert result.list.items_count == 1
    assert result.list.items[0].product_id == _PRODUCT_ID

    sfl_item_id = result.list.items[0].id
    result = sfl_ops.move_from_saved_for_later(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        cart_id=result.list.id,
        line_item_ids=[sfl_item_id],
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
    )
    assert result.list.items_count == 0
    assert result.cart.items_count == 1
    assert result.cart.items[0].product_id == _PRODUCT_ID
