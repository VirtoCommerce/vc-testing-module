import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import OrderOperations

_ADMINISTRATOR = "acme_store_administrator@acme.com"
_ORDER_NUMBER = "CO251029-00038"


@pytest.mark.graphql
@pytest.mark.with_user(_ADMINISTRATOR)
@allure.feature("Orders (GraphQL)")
@allure.title("Search organization orders by order number")
def test_organization_orders_search_by_number(graphql_client: GraphQLClient) -> None:
    with allure.step(f"Search organization orders by number '{_ORDER_NUMBER}'"):
        orders = OrderOperations(client=graphql_client).get_organization_orders(
            filter=f"number:{_ORDER_NUMBER}",
        )

    with allure.step(f"Verify exactly one order with number '{_ORDER_NUMBER}' is returned"):
        assert len(orders) == 1
        assert orders[0].number == _ORDER_NUMBER
