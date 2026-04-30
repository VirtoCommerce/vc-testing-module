from datetime import datetime, timedelta

import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import OrderOperations
from tests.context import Context

_MAINTAINER = "acme_store_maintainer_1@acme.com"

_STATUS_NEW = "New"
_STATUS_COMPLETED = "Completed"
_STATUS_PENDING = "Pending"
_STATUS_PAYMENT_REQUIRED = "Payment required"
_STATUS_READY_FOR_PICKUP = "ReadyForPickup"


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
@allure.feature("Orders (GraphQL)")
@allure.title(f"Filter organization orders by status '{_STATUS_NEW}'")
def test_orders_filter_by_status_new(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    with allure.step(f"Fetch organization orders filtered by status '{_STATUS_NEW}'"):
        orders = OrderOperations(client=graphql_client).get_organization_orders(
            organization_id=ctx.organization_id,
            filter=f"status:{_STATUS_NEW!r}",
        )

    with allure.step(f"Verify all orders have status '{_STATUS_NEW}'"):
        assert len(orders) > 0
        assert all(o.status == _STATUS_NEW for o in orders)


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
@allure.feature("Orders (GraphQL)")
@allure.title(f"Filter organization orders by status '{_STATUS_COMPLETED}'")
def test_orders_filter_by_status_completed(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    with allure.step(
        f"Fetch organization orders filtered by status '{_STATUS_COMPLETED}'"
    ):
        orders = OrderOperations(client=graphql_client).get_organization_orders(
            organization_id=ctx.organization_id,
            filter=f"status:{_STATUS_COMPLETED!r}",
        )

    with allure.step(f"Verify all orders have status '{_STATUS_COMPLETED}'"):
        assert len(orders) > 0
        assert all(o.status == _STATUS_COMPLETED for o in orders)


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
@allure.feature("Orders (GraphQL)")
@allure.title(f"Filter organization orders by status '{_STATUS_PENDING}'")
def test_orders_filter_by_status_pending(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    with allure.step(
        f"Fetch organization orders filtered by status '{_STATUS_PENDING}'"
    ):
        orders = OrderOperations(client=graphql_client).get_organization_orders(
            organization_id=ctx.organization_id,
            filter=f"status:{_STATUS_PENDING!r}",
        )

    with allure.step(f"Verify all orders have status '{_STATUS_PENDING}'"):
        assert len(orders) > 0
        assert all(o.status == _STATUS_PENDING for o in orders)


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
@allure.feature("Orders (GraphQL)")
@allure.title(f"Filter organization orders by status '{_STATUS_PAYMENT_REQUIRED}'")
def test_orders_filter_by_status_payment_required(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    with allure.step(
        f"Fetch organization orders filtered by status '{_STATUS_PAYMENT_REQUIRED}'"
    ):
        orders = OrderOperations(client=graphql_client).get_organization_orders(
            organization_id=ctx.organization_id,
            filter=f'status:"{_STATUS_PAYMENT_REQUIRED}"',
        )

    with allure.step(f"Verify all orders have status '{_STATUS_PAYMENT_REQUIRED}'"):
        assert len(orders) > 0
        assert all(o.status == _STATUS_PAYMENT_REQUIRED for o in orders)


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
@allure.feature("Orders (GraphQL)")
@allure.title(f"Filter organization orders by status '{_STATUS_READY_FOR_PICKUP}'")
def test_orders_filter_by_status_ready_for_pickup(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    with allure.step(
        f"Fetch organization orders filtered by status '{_STATUS_READY_FOR_PICKUP}'"
    ):
        orders = OrderOperations(client=graphql_client).get_organization_orders(
            organization_id=ctx.organization_id,
            filter=f"status:{_STATUS_READY_FOR_PICKUP!r}",
        )

    with allure.step(f"Verify all orders have status '{_STATUS_READY_FOR_PICKUP}'"):
        assert len(orders) > 0
        assert all(o.status == _STATUS_READY_FOR_PICKUP for o in orders)


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
@allure.feature("Orders (GraphQL)")
@allure.title("Filter organization orders by created date range")
def test_orders_filter_by_date(graphql_client: GraphQLClient, ctx: Context) -> None:
    order_ops = OrderOperations(client=graphql_client)

    with allure.step("Fetch all orders to anchor the date range"):
        # Fetch all orders to anchor the date range on actual backend-assigned dates.
        # This avoids relying on dataset dates which may differ from seeded dates.
        all_orders = order_ops.get_organization_orders(
            organization_id=ctx.organization_id
        )
        assert len(all_orders) > 0, "No orders found — check seeded data"

        anchor = datetime.fromisoformat(
            all_orders[0].created_date.replace("Z", "+00:00")
        )
        date_from = (anchor - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
        date_to = (anchor + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")

    with allure.step(f"Fetch orders in date range [{date_from} TO {date_to}]"):
        orders_in_range = order_ops.get_organization_orders(
            organization_id=ctx.organization_id,
            filter=f'createddate:["{date_from}" TO "{date_to}"]',
        )

    with allure.step("Verify returned orders fall within the date range"):
        assert len(orders_in_range) > 0
        assert all(
            datetime.fromisoformat(o.created_date.replace("Z", "+00:00"))
            >= anchor - timedelta(days=7)
            for o in orders_in_range
        )
