import time

import allure
import pytest
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import CartOperations
from gql.types import Cart, CartItemInput
from tests.context import Context

from utils.line_item_utils import has_line_item

_PRODUCT_1_ID = "smartphone-apple-iphone-17-256gb-black"
_QUANTITY_1 = 3
_PRODUCT_2_ID = "smartphone-apple-iphone-17-256gb-mist-blue"
_QUANTITY_2 = 4


@pytest.mark.graphql
@pytest.mark.flaky(retries=2, delay=3)
@allure.feature("Cart / Bulk Items (GraphQL)")
@allure.title("Add multiple products to cart in a single mutation")
def test_cart_add_bulk_items(
    graphql_client: GraphQLClient,
    ctx: Context,
    global_settings: GlobalSettings,
) -> None:
    cart_ops = CartOperations(client=graphql_client)
    cart: Cart | None = None

    try:
        with allure.step(f"Add items to cart: {_PRODUCT_1_ID}×{_QUANTITY_1}, {_PRODUCT_2_ID}×{_QUANTITY_2}"):
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

        with allure.step("Verify both products are present with the requested quantities"):
            # The addItemsCart mutation response has been observed to return
            # items=[] on mysql under load even though the items were persisted.
            # Re-read via get_cart with the storefront's lookup shape
            # (user_id, no cart_id) until items materialize.
            fetched: Cart | None = None
            for _ in range(global_settings.poll_attempts):
                fetched = cart_ops.get_cart(
                    store_id=ctx.store_id,
                    user_id=ctx.user_id,
                    currency_code=ctx.currency_code,
                    culture_name=ctx.culture_name,
                )
                if (
                    fetched
                    and fetched.id == cart.id
                    and has_line_item(fetched.items, product_id=_PRODUCT_1_ID, quantity=_QUANTITY_1)
                    and has_line_item(fetched.items, product_id=_PRODUCT_2_ID, quantity=_QUANTITY_2)
                ):
                    break
                time.sleep(global_settings.poll_interval)
            assert fetched is not None and fetched.id == cart.id, (
                f"Cart {cart.id} not visible via user_id lookup within "
                f"{global_settings.poll_attempts * global_settings.poll_interval}s"
            )
            assert has_line_item(fetched.items, product_id=_PRODUCT_1_ID, quantity=_QUANTITY_1)
            assert has_line_item(fetched.items, product_id=_PRODUCT_2_ID, quantity=_QUANTITY_2)
    finally:
        if cart is not None:
            with allure.step(f"Teardown: delete cart {cart.id}"):
                cart_ops.delete_cart(cart_id=cart.id, user_id=ctx.user_id)
