import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT


@allure.title("Clear anonymous cart (GraphQL)")
def test_clear_anonymous_cart(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to clear anonymous cart...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user = user_operations.get_me()["me"]

    cart_operations = CartOperations(graphql_client)
    cart = cart_operations.add_item_to_cart(
        store_id=config["store_id"],
        user_id=user["id"],
        product_id=TEST_PRODUCT["id"],
        quantity=1,
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )["addItem"]

    updated_cart = cart_operations.clear_cart(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )["clearCart"]

    # Test teardown
    cart_operations.remove_cart(
        cart_id=updated_cart["id"],
        user_id=user["id"],
    )

    assert updated_cart["id"] is not None
    assert updated_cart["id"] == cart["id"]
    assert updated_cart["isAnonymous"] == True
    assert updated_cart["customerId"] == user["id"]
    assert updated_cart["itemsQuantity"] == 0
