import pytest
from core.clients import GraphQLClient
from gql.operations import ShoppingListOperations
from gql.types import CartItemInput, ShoppingList
from tests.context import Context

from utils.line_item_utils import has_line_item

_USERNAME = "acme_store_employee_1@acme.com"
_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_QUANTITY = 3


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
def test_shopping_list_add_item(graphql_client: GraphQLClient, ctx: Context) -> None:
    shopping_list_ops = ShoppingListOperations(client=graphql_client)
    shopping_list: ShoppingList | None = None

    try:
        shopping_list = shopping_list_ops.create_shopping_list(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            name="TEST SHOPPING LIST",
            description="Test shopping list decription",
        )

        assert shopping_list is not None
        assert shopping_list.id is not None

        shopping_list = shopping_list_ops.add_items_to_shopping_list(
            list_id=shopping_list.id,
            items=[CartItemInput(product_id=_PRODUCT_ID, quantity=_QUANTITY)],
        )

        assert has_line_item(
            shopping_list.items, product_id=_PRODUCT_ID, quantity=_QUANTITY
        )
    finally:
        if shopping_list is not None:
            shopping_list_ops.delete_shopping_list(list_id=shopping_list.id)
