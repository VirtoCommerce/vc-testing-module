import allure
import pytest

from core.clients import GraphQLClient
from gql.operations import OrderOperations

_MAINTAINER = "acme_store_maintainer_1@acme.com"
_ORDER_NUMBER = "CO251029-00038"


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
@allure.feature("Orders (GraphQL)")
@allure.title("Get order by order number")
def test_get_order_by_number(graphql_client: GraphQLClient) -> None:
    with allure.step(f"Fetch order by number '{_ORDER_NUMBER}'"):
        order = OrderOperations(client=graphql_client).get_order(number=_ORDER_NUMBER)

    with allure.step(f"Verify returned order has number '{_ORDER_NUMBER}'"):
        assert order is not None
        assert order.number == _ORDER_NUMBER
