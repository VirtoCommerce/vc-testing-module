import allure, os, pytest
from graphql_operations.order.order_operations import OrderOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_user import TEST_PERMANENT_USER
from fixtures.auth_fixture import Auth
from fixtures.graphql_client_fixture import GraphQLClient


@pytest.mark.graphql
@allure.title("Sort orders by date (GraphQL)")
def test_sort_orders_by_date(auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to sort orders by date...", end=" ")

    user_operations = UserOperations(graphql_client)
    order_operations = OrderOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

    user = user_operations.get_user()

    search_orders_result_created_date_desc = order_operations.get_orders(
        user_id=user["id"],
        culture_name=TEST_CULTURE["en-US"],
    )

    order_dates_desc = [order["createdDate"] for order in search_orders_result_created_date_desc["items"]]
    is_sorted_desc = all(order_dates_desc[i] >= order_dates_desc[i + 1] for i in range(len(order_dates_desc) - 1))

    search_orders_result_created_date_asc = order_operations.get_orders(
        user_id=user["id"],
        culture_name=TEST_CULTURE["en-US"],
        sort="createdDate:asc",
    )

    order_dates_asc = [order["createdDate"] for order in search_orders_result_created_date_asc["items"]]
    is_sorted_asc = all(order_dates_asc[i] <= order_dates_asc[i + 1] for i in range(len(order_dates_asc) - 1))

    auth.clear_token()

    assert is_sorted_desc, "Orders are not sorted by date in descending order"
    assert is_sorted_asc, "Orders are not sorted by date in ascending order"


@pytest.mark.graphql
@allure.title("Sort orders by total amount (GraphQL)")
def test_sort_orders_by_total_amount(auth: Auth, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to sort orders by total amount...", end=" ")

    user_operations = UserOperations(graphql_client)
    order_operations = OrderOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

    user = user_operations.get_user()

    search_orders_result_total_amount_desc = order_operations.get_orders(
        user_id=user["id"], culture_name=TEST_CULTURE["en-US"], sort="total:desc"
    )

    order_totals_desc = [order["total"]["amount"] for order in search_orders_result_total_amount_desc["items"]]
    is_sorted_desc = all(order_totals_desc[i] >= order_totals_desc[i + 1] for i in range(len(order_totals_desc) - 1))

    search_orders_result_order_total_amount_asc = order_operations.get_orders(
        user_id=user["id"],
        culture_name=TEST_CULTURE["en-US"],
        sort="total:asc",
    )

    order_totals_asc = [order["total"]["amount"] for order in search_orders_result_order_total_amount_asc["items"]]
    is_sorted_asc = all(order_totals_asc[i] <= order_totals_asc[i + 1] for i in range(len(order_totals_asc) - 1))

    auth.clear_token()

    assert is_sorted_desc, "Orders are not sorted by date in descending order"
    assert is_sorted_asc, "Orders are not sorted by date in ascending order"
