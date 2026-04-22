import pytest
from core.clients import GraphQLClient
from gql.operations import OrderOperations

_ADMINISTRATOR = "acme_store_administrator@acme.com"


@pytest.mark.graphql
@pytest.mark.parametrize("sort", ["createdDate:asc", "createdDate:desc"])
@pytest.mark.with_user(_ADMINISTRATOR)
def test_organization_orders_sort_by_date(
    graphql_client: GraphQLClient, sort: str
) -> None:
    orders = OrderOperations(client=graphql_client).get_organization_orders(sort=sort)

    assert len(orders) > 1
    dates = [o.created_date for o in orders]
    assert dates == sorted(dates, reverse=sort.endswith(":desc"))


@pytest.mark.graphql
@pytest.mark.parametrize("sort", ["total:asc", "total:desc"])
@pytest.mark.with_user(_ADMINISTRATOR)
def test_organization_orders_sort_by_total(
    graphql_client: GraphQLClient, sort: str
) -> None:
    orders = OrderOperations(client=graphql_client).get_organization_orders(sort=sort)

    assert len(orders) > 1
    amounts = [o.total.amount for o in orders]
    assert amounts == sorted(amounts, reverse=sort.endswith(":desc"))
