import pytest
from core.clients import GraphQLClient
from gql.operations import CartOperations
from gql.types.cart import Cart
from tests.context import Context

_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_QTY = 1


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, _QTY)])
def test_cart_remove_item(
    graphql_client: GraphQLClient, ctx: Context, with_cart: Cart
) -> None:
    assert with_cart.items_count == _QTY
    line_item = with_cart.items[0]

    cart = CartOperations(client=graphql_client).remove_cart_item(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        cart_id=with_cart.id,
        line_item_id=line_item.id,
    )

    assert cart.items_count == 0
    assert not any(i.id == line_item.id for i in cart.items)
