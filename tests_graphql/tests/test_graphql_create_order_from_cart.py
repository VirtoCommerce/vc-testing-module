import allure, os
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT_1


@allure.title("Create order from cart (GraphQL)")
def test_create_order_from_cart(config, graphql_client):
    print(f"{os.linesep}Running test to create order from cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

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

    order = cart_operations.create_order_from_cart(
        payload={
            "cartId": cart["id"],
        }
    )

    assert order["id"] is not None, "Order ID is None"
    assert order["number"] is not None, "Order number is None"
    assert order["items"] is not None, "Order items are None"
    assert len(order["items"]) == 1, "Order items length is not 1"
    assert order["items"][0]["productId"] == TEST_PRODUCT_1["id"], "Order item product ID is not the same"
    assert order["items"][0]["quantity"] == 1, "Order item quantity is not 1"
