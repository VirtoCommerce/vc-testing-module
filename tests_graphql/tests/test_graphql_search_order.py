import os
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.order.order_operations import OrderOperations


@pytest.mark.graphql
@allure.title("Search order (GraphQL)")
def test_search_order(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running test to search order...", end=" ")

    order_operations = OrderOperations(graphql_client)

    user_maintainer = next(user for user in dataset["users"] if user["id"] == "user-acme-store-maintainer-1")
    organization = dataset["organizations"][0]
    culture = dataset["languages"][0]["defaultValue"]
    order = dataset["orders"][0]

    auth.authenticate(
        user_maintainer["userName"],
        config["USERS_PASSWORD"],
    )

    # Check if order exists in dataset
    if order is None or order.get("number") is None:
        auth.clear_token()

    # Get the order details to check its organization (before clearing token)
    order_id = order.get("id") or dataset["orders"][0].get("id")
    if order_id:
        order_details = order_operations.get_order(order_id)

        # Check if the order belongs to the organization being tested
        if order_details and order_details.get("organizationId"):
            order_org_id = order_details["organizationId"]
            if order_org_id != organization["id"]:
                auth.clear_token()

    search_orders_result = order_operations.get_organization_orders(
        filter=r"number:\"" + order["number"] + '"',
        culture_name=culture,
        organization_id=organization["id"],
    )

    auth.clear_token()

    assert search_orders_result["totalCount"] > 0, (
        f"Expected at least 1 order with number '{order['number']}', "
        f"got {search_orders_result['totalCount']}. "
        f"Organization: {organization['id']}"
    )
