import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT


@allure.title("Remove item from cart (GraphQL)")
def test_remove_item_from_cart(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to remove item from cart...", end=" ")

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

    line_item = cart["items"][0]

    updated_cart = cart_operations.remove_cart_item(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        line_item_id=line_item["id"],
    )["removeCartItem"]

    removed_line_item = next((item for item in updated_cart["items"] if item["id"] == line_item["id"]), None)

    # Test teardown
    cart_operations.remove_cart(
        cart_id=updated_cart["id"],
        user_id=user["id"],
    )

    assert updated_cart["id"] is not None
    assert updated_cart["id"] == cart["id"]
    assert updated_cart["customerId"] == user["id"]
    assert removed_line_item is None
