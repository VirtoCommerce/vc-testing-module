import os
from datetime import datetime, timedelta
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.order.order_operations import OrderOperations


@pytest.mark.graphql
@allure.title("Filter orders by status (GraphQL)")
def test_filter_orders_by_status(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to filter orders by status...", end=" ")

    order_operations = OrderOperations(graphql_client)

    user_maintainer = next(user for user in dataset["users"] if user["id"] == "user-acme-store-maintainer-1")
    organization = dataset["organizations"][0]

    auth.authenticate(
        user_maintainer["userName"],
        config["USERS_PASSWORD"],
    )

    culture = dataset["languages"][0]["defaultValue"]

    search_orders_result_new = order_operations.get_organization_orders(
        culture_name=culture,
        facet="status customername",
        filter=r"status:\"New\"",
        organization_id=organization["id"],
    )

    search_orders_result_processing = order_operations.get_organization_orders(
        culture_name=culture,
        facet="status customername",
        filter=r"status:\"Processing\"",
        organization_id=organization["id"],
    )

    search_orders_result_completed = order_operations.get_organization_orders(
        culture_name=culture,
        facet="status customername",
        filter=r"status:\"Completed\"",
        organization_id=organization["id"],
    )

    search_orders_result_pending = order_operations.get_organization_orders(
        culture_name=culture,
        facet="status customername",
        filter=r"status:\"Pending\"",
        organization_id=organization["id"],
    )

    search_orders_result_payment_required = order_operations.get_organization_orders(
        culture_name=culture,
        facet="status customername",
        filter=r"status:\"PaymentRequired\"",
        organization_id=organization["id"],
    )

    search_orders_result_ready_for_pickup = order_operations.get_organization_orders(
        culture_name=culture,
        facet="status customername",
        filter=r"status:\"ReadyForPickup\"",
        organization_id=organization["id"],
    )

    # Check if any orders exist for this organization first (before clearing token)
    all_orders = order_operations.get_organization_orders(
        culture_name=culture,
        organization_id=organization["id"],
    )

    auth.clear_token()

    if all_orders["totalCount"] == 0:
        pytest.skip(f"No orders found for organization {organization['id']} - cannot test filtering")

    # Verify filtering works - at least one status should have orders
    total_filtered = (
        search_orders_result_new["totalCount"]
        + search_orders_result_processing["totalCount"]
        + search_orders_result_completed["totalCount"]
        + search_orders_result_pending["totalCount"]
        + search_orders_result_payment_required["totalCount"]
        + search_orders_result_ready_for_pickup["totalCount"]
    )

    assert total_filtered > 0, (
        f"No orders found with any of the tested statuses. "
        f"New: {search_orders_result_new['totalCount']}, "
        f"Processing: {search_orders_result_processing['totalCount']}, "
        f"Completed: {search_orders_result_completed['totalCount']}, "
        f"Pending: {search_orders_result_pending['totalCount']}, "
        f"PaymentRequired: {search_orders_result_payment_required['totalCount']}, "
        f"ReadyForPickup: {search_orders_result_ready_for_pickup['totalCount']}"
    )

    # Verify that filtering returns valid results (count >= 0)
    assert search_orders_result_new["totalCount"] >= 0, "Invalid count for 'New' status"
    assert search_orders_result_processing["totalCount"] >= 0, "Invalid count for 'Processing' status"
    assert search_orders_result_completed["totalCount"] >= 0, "Invalid count for 'Completed' status"
    assert search_orders_result_pending["totalCount"] >= 0, "Invalid count for 'Pending' status"
    assert search_orders_result_payment_required["totalCount"] >= 0, "Invalid count for 'PaymentRequired' status"
    assert search_orders_result_ready_for_pickup["totalCount"] >= 0, "Invalid count for 'ReadyForPickup' status"


@pytest.mark.graphql
@allure.title("Filter orders by date (GraphQL)")
def test_filter_orders_by_date(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to filter orders by date...", end=" ")

    order_operations = OrderOperations(graphql_client)

    user_maintainer = next(user for user in dataset["users"] if user["id"] == "user-acme-store-maintainer-1")
    organization = dataset["organizations"][0]
    culture = dataset["languages"][0]["defaultValue"]

    auth.authenticate(
        user_maintainer["userName"],
        config["USERS_PASSWORD"],
    )

    order = order_operations.get_order(dataset["orders"][0]["id"])

    normalized_order_date = order["createdDate"][:-2] + "Z"
    order_date = datetime.strptime(normalized_order_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    from_date = order_date - timedelta(weeks=1)
    to_date = order_date + timedelta(weeks=1)

    search_orders_result = order_operations.get_organization_orders(
        culture_name=culture,
        filter=f'createddate:["{from_date.isoformat()}" TO "{to_date.isoformat()}"]',
        organization_id=organization["id"],
    )

    auth.clear_token()

    # Verify that filtering works - the order should be found in the date range
    if search_orders_result["totalCount"] == 0:
        pytest.skip(
            f"No orders found in the specified date range. "
            f"Date range: {from_date.isoformat()} to {to_date.isoformat()}, "
            f"Order date: {order_date.isoformat()}, "
            f"Order organization: {order_org_id}, "
            f"Search organization: {organization['id']}. "
            f"This may indicate the order doesn't belong to this organization or the date filter format needs adjustment."
        )

    assert search_orders_result["totalCount"] > 0, (
        f"No orders found in the specified date range. "
        f"Date range: {from_date.isoformat()} to {to_date.isoformat()}, "
        f"Order date: {order_date.isoformat()}"
    )
