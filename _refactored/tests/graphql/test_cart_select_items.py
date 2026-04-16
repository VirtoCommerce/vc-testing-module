import pytest

from core.clients import GraphQLClient
from gql.operations import CartOperations
from gql.types.cart import Cart
from tests.context import Context

_PRODUCT_ID_1 = "product-acme-laptop-asus-zenbook-a14-ux3407"
_PRODUCT_ID_2 = "product-acme-product2-main1-stock"


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID_1, 1), (_PRODUCT_ID_2, 1)])
def test_cart_unselect_item(
    graphql_client: GraphQLClient, ctx: Context, with_cart: Cart
) -> None:
    assert all(item.selected_for_checkout for item in with_cart.items)

    cart_ops = CartOperations(client=graphql_client)
    item_to_unselect = with_cart.items[0]

    cart = cart_ops.unselect_cart_items(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        cart_id=with_cart.id,
        line_item_ids=[item_to_unselect.id],
    )

    unselected = next(i for i in cart.items if i.id == item_to_unselect.id)
    remaining = next(i for i in cart.items if i.id != item_to_unselect.id)
    assert unselected.selected_for_checkout is False
    assert remaining.selected_for_checkout is True


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID_1, 1), (_PRODUCT_ID_2, 1)])
def test_cart_select_item(
    graphql_client: GraphQLClient, ctx: Context, with_cart: Cart
) -> None:
    cart_ops = CartOperations(client=graphql_client)

    cart = cart_ops.unselect_all_cart_items(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        cart_id=with_cart.id,
    )
    assert all(not item.selected_for_checkout for item in cart.items)

    item_to_select = cart.items[0]
    cart = cart_ops.select_cart_items(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        cart_id=with_cart.id,
        line_item_ids=[item_to_select.id],
    )

    selected = next(i for i in cart.items if i.id == item_to_select.id)
    remaining = next(i for i in cart.items if i.id != item_to_select.id)
    assert selected.selected_for_checkout is True
    assert remaining.selected_for_checkout is False
