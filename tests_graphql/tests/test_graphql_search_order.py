import allure, os
from tests_graphql.operations.order.order_operations import OrderOperations
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_user import TEST_PERMANENT_USER
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_order import TEST_ORDER_1


@allure.title("Search order (GraphQL)")
def test_search_order(config, user_service, graphql_client):
    print(f"{os.linesep}Running test to search order...", end=" ")

    user_operations = UserOperations(graphql_client)
    order_operations = OrderOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

    user = user_operations.get_user()

    search_orders_result = order_operations.get_orders(
        user_id=user["id"],
        filter=TEST_ORDER_1["number"],
        culture_name=TEST_CULTURE["en-US"],
    )

    user_service.sign_out()

    assert search_orders_result["totalCount"] == 1, f"Expected 1 order, got {search_orders_result['totalCount']}"
    assert (
        search_orders_result["items"][0]["customerId"] == user["id"]
    ), f"Expected customer ID {user['id']}, got {search_orders_result['items'][0]['customerId']}"
    assert (
        search_orders_result["items"][0]["number"] == TEST_ORDER_1["number"]
    ), f"Expected order number {TEST_ORDER_1['number']}, got {search_orders_result['items'][0]['number']}"
