import allure, os, pytest
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_user import TEST_ADMIN_USER


@pytest.mark.graphql
@allure.title("Get anonymous cart (GraphQL)")
def test_get_anonymous_cart(config, graphql_client):
    print(f"{os.linesep}Running test to get anonymous cart...", end=" ")

    user_operations = UserOperations(graphql_client)
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


@pytest.mark.graphql
@allure.title("Get registered user cart (GraphQL)")
def test_get_registered_user_cart(config, auth, graphql_client):
    print(f"{os.linesep}Running test to get registered user cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

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

    auth.clear_token()

    assert cart["id"] is not None, "Cart ID is None"
    assert cart["isAnonymous"] == False, "Cart is anonymous"
    assert cart["customerId"] == user["id"], "Cart customer ID is not the same"
