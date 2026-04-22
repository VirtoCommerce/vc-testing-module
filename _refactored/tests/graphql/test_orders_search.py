import pytest
from core.clients import GraphQLClient
from gql.operations import OrderOperations

_ADMINISTRATOR = "acme_store_administrator@acme.com"
_ORDER_NUMBER = "CO251029-00038"


@pytest.mark.graphql
@pytest.mark.with_user(_ADMINISTRATOR)
def test_organization_orders_search_by_number(graphql_client: GraphQLClient) -> None:
    orders = OrderOperations(client=graphql_client).get_organization_orders(
        filter=f"number:{_ORDER_NUMBER}",
    )

    assert len(orders) == 1
    assert orders[0].number == _ORDER_NUMBER
