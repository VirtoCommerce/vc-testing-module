import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT


@allure.title("Add item to anonymous cart (GraphQL)")
def test_get_registered_user_cart(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to add item to anonymous cart...", end=" ")

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

    cart_operations.clear_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    assert add_item_response["addItem"]["id"] is not None
    assert add_item_response["addItem"]["customerId"] == user_response["me"]["id"]
    assert add_item_response["addItem"]["itemsQuantity"] == 1
