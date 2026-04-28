import pytest
from core.clients import GraphQLClient
from gql.operations import ShoppingListOperations
from gql.types import ShoppingList
from tests.context import Context

_USERNAME = "acme_store_employee_1@acme.com"
_LIST_NAME = "My Test List"


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
def test_shopping_list_manage(graphql_client: GraphQLClient, ctx: Context) -> None:
    shopping_list_ops = ShoppingListOperations(client=graphql_client)
    shopping_list: ShoppingList | None = None

    try:
        shopping_list = shopping_list_ops.create_shopping_list(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            name=_LIST_NAME,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
        )

        assert shopping_list.id is not None
        assert shopping_list.name == _LIST_NAME
        assert shopping_list.store_id == ctx.store_id
        assert shopping_list.items == []

        fetched = shopping_list_ops.get_shopping_list(list_id=shopping_list.id)
        assert fetched.id == shopping_list.id
        assert fetched.name == _LIST_NAME
    finally:
        if shopping_list is not None and shopping_list.id is not None:
            shopping_list_ops.delete_shopping_list(list_id=shopping_list.id)
