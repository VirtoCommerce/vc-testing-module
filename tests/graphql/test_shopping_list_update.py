import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import ShoppingListOperations
from tests.context import Context

_USERNAME = "acme_store_employee_1@acme.com"
_LIST_NAME = "Test Update List"
_UPDATED_NAME = "Updated List Name"
_UPDATED_DESCRIPTION = "Updated description"
_UPDATED_SCOPE = "Organization"


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@allure.feature("Shopping Lists (GraphQL)")
@allure.title("Update shopping list name, description, and scope")
def test_shopping_list_update(graphql_client: GraphQLClient, ctx: Context) -> None:
    ops = ShoppingListOperations(client=graphql_client)
    shopping_list = None

    try:
        with allure.step(f"Create shopping list '{_LIST_NAME}'"):
            shopping_list = ops.create_shopping_list(
                store_id=ctx.store_id,
                user_id=ctx.user_id,
                name=_LIST_NAME,
                currency_code=ctx.currency_code,
                culture_name=ctx.culture_name,
            )

        with allure.step(
            f"Change shopping list to name '{_UPDATED_NAME}', scope '{_UPDATED_SCOPE}'"
        ):
            updated = ops.change_shopping_list(
                list_id=shopping_list.id,
                name=_UPDATED_NAME,
                description=_UPDATED_DESCRIPTION,
                scope=_UPDATED_SCOPE,
            )

        with allure.step(
            "Verify shopping list reflects updated name, description, and scope"
        ):
            assert updated.name == _UPDATED_NAME
            assert updated.description == _UPDATED_DESCRIPTION
            assert updated.sharing_setting is not None
            assert updated.sharing_setting.scope == _UPDATED_SCOPE
    finally:
        if shopping_list is not None:
            with allure.step(f"Teardown: delete shopping list {shopping_list.id}"):
                ops.delete_shopping_list(list_id=shopping_list.id)
