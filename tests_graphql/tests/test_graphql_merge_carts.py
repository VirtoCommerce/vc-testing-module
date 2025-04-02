import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT, TEST_PRODUCT_2


@allure.title("Merge carts (GraphQL)")
def test_merge_carts(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to merge carts...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    cart_operations = CartOperations(graphql_client)

    anonymous_user = user_operations.get_me()["me"]
    anonymous_cart = cart_operations.add_item_to_cart(
        store_id=config["store_id"],
        user_id=anonymous_user["id"],
        product_id=TEST_PRODUCT["id"],
        quantity=1,
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )["addItem"]

    registered_user = user_operations.get_me(auth_required=True)["me"]
    registered_user_cart = cart_operations.add_item_to_cart(
        store_id=config["store_id"],
        user_id=registered_user["id"],
        product_id=TEST_PRODUCT_2["id"],
        quantity=2,
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )["addItem"]

    merged_cart = cart_operations.merge_cart(
        store_id=config["store_id"],
        user_id=registered_user["id"],
        second_cart_id=anonymous_cart["id"],
        culture_name=TEST_CULTURE["en-US"],
        currency_code=TEST_CURRENCY["USD"],
        delete_after_merge=True,
    )["mergeCart"]

    # Test teardown
    cart_operations.remove_cart(
        cart_id=registered_user_cart["id"],
        user_id=registered_user["id"],
    )

    assert merged_cart["id"] is not None
    assert merged_cart["id"] == registered_user_cart["id"]
    assert merged_cart["itemsQuantity"] == 3
