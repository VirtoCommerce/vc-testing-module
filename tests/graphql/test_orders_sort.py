import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import OrderOperations

_ADMINISTRATOR = "acme_store_administrator@acme.com"


@pytest.mark.graphql
@pytest.mark.parametrize("sort", ["createdDate:asc", "createdDate:desc"])
@pytest.mark.with_user(_ADMINISTRATOR)
@allure.feature("Orders (GraphQL)")
@allure.title("Sort organization orders by created date")
def test_organization_orders_sort_by_date(
    graphql_client: GraphQLClient, sort: str
) -> None:
    with allure.step(f"Fetch organization orders sorted by '{sort}'"):
        orders = OrderOperations(client=graphql_client).get_organization_orders(
            sort=sort
        )

    with allure.step(f"Verify orders are sorted by date '{sort}'"):
        assert len(orders) > 1
        dates = [o.created_date for o in orders]
        assert dates == sorted(dates, reverse=sort.endswith(":desc"))


@pytest.mark.graphql
@pytest.mark.parametrize("sort", ["total:asc", "total:desc"])
@pytest.mark.with_user(_ADMINISTRATOR)
@allure.feature("Orders (GraphQL)")
@allure.title("Sort organization orders by total")
def test_organization_orders_sort_by_total(
    graphql_client: GraphQLClient, sort: str
) -> None:
    with allure.step(f"Fetch organization orders sorted by '{sort}'"):
        orders = OrderOperations(client=graphql_client).get_organization_orders(
            sort=sort
        )

    with allure.step(f"Verify orders are sorted by total '{sort}'"):
        assert len(orders) > 1
        amounts = [o.total.amount for o in orders]
        assert amounts == sorted(amounts, reverse=sort.endswith(":desc"))
