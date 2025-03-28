import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT


@allure.title("Change cart item quantity (GraphQL)")
def test_get_registered_user_cart(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to change cart item quantity...", end=" ")

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

    line_item = add_item_response["addItem"]["items"][0]

    change_cart_item_quantity_response = cart_operations.change_cart_item_quantity(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        line_item_id=line_item["id"],
        quantity=10,
    )

    cart_operations.clear_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    assert change_cart_item_quantity_response["changeCartItemQuantity"]["id"] is not None
    assert change_cart_item_quantity_response["changeCartItemQuantity"]["customerId"] == user_response["me"]["id"]
    assert change_cart_item_quantity_response["changeCartItemQuantity"]["itemsQuantity"] == 10
