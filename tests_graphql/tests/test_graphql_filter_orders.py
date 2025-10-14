import os
from datetime import timedelta
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from graphql_operations.order.order_operations import OrderOperations


@pytest.mark.graphql
@allure.title("Filter orders by status (GraphQL)")
def test_filter_orders_by_status(
    config: dict[str, Any],
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to filter orders by status...", end=" ")

    order_operations = OrderOperations(graphql_client)

    user_maintainer = next(
        user
        for user in dataset["users"]
        if user["id"] == "user-acme-store-maintainer-1"
    )
    organization = dataset["organizations"][0]

    auth.authenticate(
        user_maintainer["userName"],
        config["users_password"],
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

    auth.clear_token()

    assert (
        search_orders_result_new["totalCount"] > 0
    ), "No orders found with status 'New'"
    assert (
        search_orders_result_processing["totalCount"] > 0
    ), "No orders found with status 'Processing'"
    assert (
        search_orders_result_completed["totalCount"] > 0
    ), "No orders found with status 'Completed'"
    assert (
        search_orders_result_pending["totalCount"] > 0
    ), "No orders found with status 'Pending'"
    assert (
        search_orders_result_payment_required["totalCount"] > 0
    ), "No orders found with status 'Payment required'"
    assert (
        search_orders_result_ready_for_pickup["totalCount"] > 0
    ), "No orders found with status 'ReadyForPickup'"


@pytest.mark.graphql
@allure.title("Filter orders by date (GraphQL)")
def test_filter_orders_by_date(
    config: dict[str, Any],
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to filter orders by date...", end=" ")

    order_operations = OrderOperations(graphql_client)

    user_maintainer = next(
        user
        for user in dataset["users"]
        if user["id"] == "user-acme-store-maintainer-1"
    )
    organization = dataset["organizations"][0]
    culture = dataset["languages"][0]["defaultValue"]

    auth.authenticate(
        user_maintainer["userName"],
        config["users_password"],
    )

    from_date = dataset["createdDate"] - timedelta(weeks=1)
    to_date = dataset["createdDate"] + timedelta(weeks=1)

    search_orders_result = order_operations.get_organization_orders(
        culture_name=culture,
        filter=f'createddate:["{from_date.isoformat()}" TO "{to_date.isoformat()}"]',
        organization_id=organization["id"],
    )

    auth.clear_token()

    assert (
        search_orders_result["totalCount"] > 0
    ), "No orders found in the specified date range"
