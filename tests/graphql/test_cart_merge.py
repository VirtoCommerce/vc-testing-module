from typing import Any

import pytest
from core.auth import AuthProvider
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import CartOperations
from gql.types.cart import Cart
from tests.context import Context

from utils.line_item_utils import has_line_item

_USER = "acme_store_employee_1@acme.com"
_PRODUCT_ID_1 = "smartphone-apple-iphone-17-256gb-black"
_PRODUCT_ID_2 = "smartphone-apple-iphone-17-256gb-mist-blue"
_QTY_1 = 2
_QTY_2 = 1


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID_1, _QTY_1), (_PRODUCT_ID_2, _QTY_2)])
def test_cart_merge(
    with_cart: Cart,
    with_user: AuthProvider,
    graphql_client: GraphQLClient,
    ctx: Context,
    dataset: dict[str, list[dict[str, Any]]],
    global_settings: GlobalSettings,
) -> None:
    anon_cart = with_cart

    user = next(u for u in dataset["users"] if u["userName"] == _USER)
    user_id = user["id"]

    with_user.sign_in(_USER, global_settings.users_password)

    cart_ops = CartOperations(client=graphql_client)
    merged_cart = cart_ops.merge_cart(
        store_id=ctx.store_id,
        user_id=user_id,
        second_cart_id=anon_cart.id,
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
    )
    try:
        assert merged_cart.items_count == 2
        assert has_line_item(merged_cart.items, _PRODUCT_ID_1, _QTY_1)
        assert has_line_item(merged_cart.items, _PRODUCT_ID_2, _QTY_2)
    finally:
        cart_ops.delete_cart(cart_id=merged_cart.id, user_id=user_id)
