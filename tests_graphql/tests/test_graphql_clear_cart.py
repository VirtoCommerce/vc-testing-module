import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT


@allure.title("Clear anonymous cart (GraphQL)")
def test_clear_anonymous_cart(config, graphql_client):
    print(f"{os.linesep}Running test to clear anonymous cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    user_response = user_operations.get_me()

    cart_operations = CartOperations(graphql_client)
    cart_operations.add_item_to_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        product_id=TEST_PRODUCT["id"],
        quantity=1,
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    clear_cart_response = cart_operations.clear_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    assert clear_cart_response["clearCart"]["id"] is not None
    assert clear_cart_response["clearCart"]["isAnonymous"] == True
    assert clear_cart_response["clearCart"]["customerId"] == user_response["me"]["id"]
    assert clear_cart_response["clearCart"]["itemsQuantity"] == 0
