import os

import allure
import pytest

from fixtures import Auth, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.order.order_operations import OrderOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_order import TEST_ORDER_1
from test_data.test_user import TEST_PERMANENT_USER


@pytest.mark.graphql
@allure.title("Search order (GraphQL)")
def test_search_order(auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to search order...", end=" ")

    user_operations = UserOperations(graphql_client)
    order_operations = OrderOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

    user = user_operations.get_user()

    search_orders_result = order_operations.get_orders(
        user_id=user["id"],
        filter=TEST_ORDER_1["number"],
        culture_name=TEST_CULTURE["en-US"],
    )

    auth.clear_token()

    assert (
        search_orders_result["totalCount"] == 1
    ), f"Expected 1 order, got {search_orders_result['totalCount']}"
    assert (
        search_orders_result["items"][0]["customerId"] == user["id"]
    ), f"Expected customer ID {user['id']}, got {search_orders_result['items'][0]['customerId']}"
    assert (
        search_orders_result["items"][0]["number"] == TEST_ORDER_1["number"]
    ), f"Expected order number {TEST_ORDER_1['number']}, got {search_orders_result['items'][0]['number']}"
