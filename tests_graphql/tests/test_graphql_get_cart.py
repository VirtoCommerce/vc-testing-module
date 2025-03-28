import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY


@allure.title("Get anonymous cart (GraphQL)")
def test_get_anonymous_cart(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to get anonymous cart...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user_response = user_operations.get_me()

    cart_operations = CartOperations(graphql_client)
    cart_response = cart_operations.get_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    assert cart_response["cart"]["id"] is not None
    assert cart_response["cart"]["isAnonymous"] == True
    assert cart_response["cart"]["customerId"] == user_response["me"]["id"]


@allure.title("Get registered user cart (GraphQL)")
def test_get_registered_user_cart(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to get registered user cart...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user_response = user_operations.get_me(auth_required=True)

    cart_operations = CartOperations(graphql_client)
    cart_response = cart_operations.get_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    assert cart_response["cart"]["id"] is not None
    assert cart_response["cart"]["isAnonymous"] == False
    assert cart_response["cart"]["customerId"] == user_response["me"]["id"]
