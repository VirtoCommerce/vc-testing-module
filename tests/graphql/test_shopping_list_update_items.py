import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import ShoppingListOperations
from gql.types.cart_item_input import CartItemInput
from tests.context import Context

_USERNAME = "acme_store_employee_1@acme.com"
_LIST_NAME = "Test Update Items List"
_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_INITIAL_QTY = 1
_UPDATED_QTY = 3


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@allure.feature("Shopping Lists (GraphQL)")
@allure.title("Update a line item quantity in a shopping list")
def test_shopping_list_update_items(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    ops = ShoppingListOperations(client=graphql_client)
    shopping_list = None

    try:
        with allure.step(
            f"Create shopping list '{_LIST_NAME}' and add {_PRODUCT_ID}×{_INITIAL_QTY}"
        ):
            shopping_list = ops.create_shopping_list(
                store_id=ctx.store_id,
                user_id=ctx.user_id,
                name=_LIST_NAME,
                currency_code=ctx.currency_code,
                culture_name=ctx.culture_name,
            )
            shopping_list = ops.add_items_to_shopping_list(
                list_id=shopping_list.id,
                items=[CartItemInput(product_id=_PRODUCT_ID, quantity=_INITIAL_QTY)],
            )

            line_item = shopping_list.items[0]
            assert line_item.quantity == _INITIAL_QTY

        with allure.step(
            f"Update line item {line_item.id} quantity to {_UPDATED_QTY}"
        ):
            shopping_list = ops.update_shopping_list_items(
                list_id=shopping_list.id,
                items=[(line_item.id, _UPDATED_QTY)],
            )

        with allure.step(
            f"Verify line item quantity is now {_UPDATED_QTY}"
        ):
            updated_item = next(i for i in shopping_list.items if i.id == line_item.id)
            assert updated_item.quantity == _UPDATED_QTY
    finally:
        if shopping_list is not None:
            with allure.step(f"Teardown: delete shopping list {shopping_list.id}"):
                ops.delete_shopping_list(list_id=shopping_list.id)
