import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.order.order_operations import OrderOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.orders_test_data import OrdersTestData
from tests_graphql.test_data.test_product import TEST_PRODUCT
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_culture import TEST_CULTURE


@allure.title("Get order details (GraphQL)")
def test_get_order(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to get order details...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user_response = user_operations.get_me()

    cart_operations = CartOperations(graphql_client)
    add_item_response = cart_operations.add_item_to_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        product_id=TEST_PRODUCT["id"],
        quantity=1,
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    create_order_from_cart_response = cart_operations.create_order_from_cart(add_item_response["addItem"]["id"])

    order_operations = OrderOperations(auth_token, graphql_client)
    order_response = order_operations.get_order(create_order_from_cart_response["createOrderFromCart"]["id"])

    assert order_response["order"]["id"] == create_order_from_cart_response["createOrderFromCart"]["id"]
    assert order_response["order"]["number"] is not None
    assert order_response["order"]["items"] is not None
    assert order_response["order"]["items"][0]["productId"] == TEST_PRODUCT["id"]
    assert order_response["order"]["items"][0]["quantity"] == 1
