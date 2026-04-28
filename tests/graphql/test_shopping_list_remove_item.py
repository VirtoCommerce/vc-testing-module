import pytest
from core.clients import GraphQLClient
from gql.operations import ShoppingListOperations
from gql.types.cart_item_input import CartItemInput
from tests.context import Context

_USERNAME = "acme_store_employee_1@acme.com"
_LIST_NAME = "Test Remove Item List"
_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_QTY = 1


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
def test_shopping_list_remove_item(graphql_client: GraphQLClient, ctx: Context) -> None:
    ops = ShoppingListOperations(client=graphql_client)
    shopping_list = None

    try:
        shopping_list = ops.create_shopping_list(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            name=_LIST_NAME,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
        )
        shopping_list = ops.add_items_to_shopping_list(
            list_id=shopping_list.id,
            items=[CartItemInput(product_id=_PRODUCT_ID, quantity=_QTY)],
        )

        assert shopping_list.items_count == _QTY
        line_item = shopping_list.items[0]

        shopping_list = ops.remove_items_from_shopping_list(
            list_id=shopping_list.id,
            line_item_ids=[line_item.id],
        )

        assert shopping_list.items_count == 0
        assert not any(i.id == line_item.id for i in shopping_list.items)
    finally:
        if shopping_list is not None:
            ops.delete_shopping_list(list_id=shopping_list.id)
