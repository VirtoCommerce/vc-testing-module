import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import CartOperations
from gql.types import Cart, CartItemInput
from tests.context import Context

from utils.line_item_utils import has_line_item

_PRODUCT_1_ID = "smartphone-apple-iphone-17-256gb-black"
_QUANTITY_1 = 3
_PRODUCT_2_ID = "smartphone-apple-iphone-17-256gb-mist-blue"
_QUANTITY_2 = 4


@pytest.mark.graphql
@allure.feature("Cart / Bulk Items (GraphQL)")
@allure.title("Add multiple products to cart in a single mutation")
def test_cart_add_bulk_items(graphql_client: GraphQLClient, ctx: Context) -> None:
    cart_ops = CartOperations(client=graphql_client)
    cart: Cart | None = None

    try:
        with allure.step(
            f"Add items to cart: {_PRODUCT_1_ID}×{_QUANTITY_1}, {_PRODUCT_2_ID}×{_QUANTITY_2}"
        ):
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
            assert has_line_item(cart.items, product_id=_PRODUCT_1_ID, quantity=_QUANTITY_1)
            assert has_line_item(cart.items, product_id=_PRODUCT_2_ID, quantity=_QUANTITY_2)
    finally:
        if cart is not None:
            with allure.step(f"Teardown: delete cart {cart.id}"):
                cart_ops.delete_cart(cart_id=cart.id, user_id=ctx.user_id)
