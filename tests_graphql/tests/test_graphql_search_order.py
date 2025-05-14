import allure, os
from tests_graphql.operations.order.order_operations import OrderOperations
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_user import TEST_PERMANENT_USER
from tests_graphql.test_data.test_product import TEST_PRODUCT_1
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_culture import TEST_CULTURE


@allure.title("Search order (GraphQL)")
def test_search_order(config, user_service, graphql_client):
    print(f"{os.linesep}Running test to search order...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    order_operations = OrderOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

    user = user_operations.get_user()

    print(user)

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "productId": TEST_PRODUCT_1["id"],
            "quantity": 1,
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
        }
    )

    created_order = cart_operations.create_order_from_cart(
        payload={
            "cartId": cart["id"],
        }
    )

    search_orders_result = order_operations.get_orders(
        user_id=user["id"],
        filter=created_order["number"],
        culture_name=TEST_CULTURE["en-US"],
    )

    user_service.sign_out()

    assert search_orders_result["totalCount"] == 1, f"Expected 1 order, got {search_orders_result['totalCount']}"
    assert (
        search_orders_result["items"][0]["customerId"] == user["id"]
    ), f"Expected customer ID {user['id']}, got {search_orders_result['items'][0]['customerId']}"
    assert (
        search_orders_result["items"][0]["number"] == created_order["number"]
    ), f"Expected order number {created_order['number']}, got {search_orders_result['items'][0]['number']}"
