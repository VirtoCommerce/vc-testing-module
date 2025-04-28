import allure, os
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY


@allure.title("Get anonymous cart (GraphQL)")
def test_get_anonymous_cart(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to get anonymous cart...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    cart = cart_operations.get_cart(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    assert cart["id"] is not None, "Cart ID is None"
    assert cart["isAnonymous"] == True, "Cart is not anonymous"
    assert cart["customerId"] == user["id"], "Cart customer ID is not the same"


@allure.title("Get registered user cart (GraphQL)")
def test_get_registered_user_cart(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to get registered user cart...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user(auth_required=True)

    cart = cart_operations.get_cart(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    assert cart["id"] is not None, "Cart ID is None"
    assert cart["isAnonymous"] == False, "Cart is anonymous"
    assert cart["customerId"] == user["id"], "Cart customer ID is not the same"
