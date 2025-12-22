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

    user_maintainer = next(
        user
        for user in dataset["users"]
        if user["id"] == "user-acme-store-maintainer-1"
    )
    organization = dataset["organizations"][0]
    culture = dataset["languages"][0]["defaultValue"]
    order = dataset["orders"][0]

    auth.authenticate(
        user_maintainer["userName"],
        config["USERS_PASSWORD"],
    )

    search_orders_result = order_operations.get_organization_orders(
        filter=r"number:\"" + order["number"] + '"',
        culture_name=culture,
        organization_id=organization["id"],
    )

    auth.clear_token()

    assert (
        search_orders_result["totalCount"] > 0
    ), f"Expected 1 order, got {search_orders_result['totalCount']}"
