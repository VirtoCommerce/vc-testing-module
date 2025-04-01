import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT, TEST_PRODUCT_2


@allure.title("Add items to anonymous cart (GraphQL)")
def test_add_items_to_anonymous_cart(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to add items to anonymous cart...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user_response = user_operations.get_me()

    user = user_response["me"]

    cart_operations = CartOperations(graphql_client)
    add_items_cart_response = cart_operations.add_items_to_cart(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        cart_items=[
            {
                "productId": TEST_PRODUCT["id"],
                "quantity": 5,
            },
            {
                "productId": TEST_PRODUCT_2["id"],
                "quantity": 10,
            },
        ],
    )

    cart = add_items_cart_response["addItemsCart"]

    # Test teardown
    cart_operations.remove_cart(
        store_id=config["store_id"],
        user_id=user["id"],
    )

    assert cart["id"] is not None
    assert cart["customerId"] == user["id"]
    assert cart["itemsQuantity"] == 15
