import allure, os, pytest
from graphql_operations.order.order_operations import OrderOperations
from graphql_operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_user import TEST_PERMANENT_USER


@pytest.mark.graphql
@allure.title("Filter orders by status (GraphQL)")
def test_filter_orders_by_status(auth, graphql_client):
    print(f"{os.linesep}Running test to filter orders by status...", end=" ")

    user_operations = UserOperations(graphql_client)
    order_operations = OrderOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

    user = user_operations.get_user()

    search_orders_result_new = order_operations.get_orders(
        user_id=user["id"], culture_name=TEST_CULTURE["en-US"], filter='status:"New"'
    )

    search_orders_result_processing = order_operations.get_orders(
        user_id=user["id"], culture_name=TEST_CULTURE["en-US"], filter='status:"Processing"'
    )

    search_orders_result_completed = order_operations.get_orders(
        user_id=user["id"], culture_name=TEST_CULTURE["en-US"], filter='status:"Completed"'
    )

    auth.clear_token()

    assert search_orders_result_new["totalCount"] > 0, "No orders found with status 'New'"
    assert search_orders_result_processing["totalCount"] > 0, "No orders found with status 'Processing'"
    assert search_orders_result_completed["totalCount"] > 0, "No orders found with status 'Completed'"


@pytest.mark.graphql
@allure.title("Filter orders by date (GraphQL)")
def test_filter_orders_by_date(auth, graphql_client):
    print(f"{os.linesep}Running test to filter orders by date...", end=" ")

    user_operations = UserOperations(graphql_client)
    order_operations = OrderOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

    user = user_operations.get_user()

    search_orders_result = order_operations.get_orders(
        user_id=user["id"],
        culture_name=TEST_CULTURE["en-US"],
        filter='createddate:["2025-05-13T22:00:00.000Z" TO "2025-05-14T21:59:59.999Z"]',
    )

    auth.clear_token()

    assert search_orders_result["totalCount"] > 0, "No orders found in the specified date range"
