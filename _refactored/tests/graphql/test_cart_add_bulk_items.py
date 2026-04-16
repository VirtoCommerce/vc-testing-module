import pytest

from core.clients import GraphQLClient
from gql.operations import CartOperations
from gql.types import Cart, CartItemInput
from tests.context import Context
from utils.line_item_utils import has_line_item

_PRODUCT_1_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"
_QUANTITY_1 = 3
_PRODUCT_2_ID = "product-acme-laptop-asus-vivobook-16-x1607qa"
_QUANTITY_2 = 4


@pytest.mark.graphql
def test_cart_add_bulk_items(graphql_client: GraphQLClient, ctx: Context) -> None:
    cart_ops = CartOperations(client=graphql_client)
    cart: Cart | None = None

    try:
        cart = cart_ops.add_items_to_cart(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            items=[
                CartItemInput(product_id=_PRODUCT_1_ID, quantity=_QUANTITY_1),
                CartItemInput(product_id=_PRODUCT_2_ID, quantity=_QUANTITY_2),
            ],
        )

        assert has_line_item(cart.items, product_id=_PRODUCT_1_ID, quantity=_QUANTITY_1)
        assert has_line_item(cart.items, product_id=_PRODUCT_2_ID, quantity=_QUANTITY_2)
    finally:
        if cart is not None:
            cart_ops.delete_cart(cart_id=cart.id, user_id=ctx.user_id)
