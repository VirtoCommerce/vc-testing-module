import pytest

from core.clients import GraphQLClient
from gql.operations import OrderOperations

_MAINTAINER = "acme_store_maintainer_1@acme.com"
_ORDER_NUMBER = "CO251029-00038"


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
def test_get_order_by_number(graphql_client: GraphQLClient) -> None:
    order = OrderOperations(client=graphql_client).get_order(number=_ORDER_NUMBER)

    assert order is not None
    assert order.number == _ORDER_NUMBER
