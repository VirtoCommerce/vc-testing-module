import allure, os, pytest
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT_1, TEST_PRODUCT_2


@pytest.mark.graphql
@allure.title("Add items to anonymous cart (GraphQL)")
def test_add_items_to_anonymous_cart(config, graphql_client):
    print(f"{os.linesep}Running test to add items to anonymous cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    user = user_operations.get_user()

    cart_operations = CartOperations(graphql_client)
    cart = cart_operations.add_items_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "cartItems": [
                {
                    "productId": TEST_PRODUCT_1["id"],
                    "quantity": 5,
                },
                {
                    "productId": TEST_PRODUCT_2["id"],
                    "quantity": 10,
                },
            ],
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    assert cart["id"] is not None, "Cart ID is None"
    assert cart["customerId"] == user["id"], "Customer ID is not the same"
    assert cart["itemsQuantity"] == 15, "Items quantity is not the same"
