import pytest

from core.clients import GraphQLClient
from gql.operations import CartOperations
from gql.types import Cart
from tests.context import Context

_PRODUCT_ID = "product-acme-laptop-asus-vivobook-16-x1607qa"
_QUANTITY = 3


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
def test_cart_clear(
    graphql_client: GraphQLClient, ctx: Context, with_cart: Cart
) -> None:
    cart_ops = CartOperations(client=graphql_client)

    cart = cart_ops.clear_cart(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        cart_id=with_cart.id,
    )

    assert cart is not None
    assert cart.items_count == 0
