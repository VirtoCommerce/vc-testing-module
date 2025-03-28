import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT, TEST_PRODUCT_2


@allure.title("Select cart items (GraphQL)")
def test_select_cart_items(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to select cart items...", end=" ")

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

    select_cart_items_response = cart_operations.select_cart_items(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        line_item_ids=[line_item["id"]],
    )

    line_item = select_cart_items_response["selectCartItems"]["items"][0]

    cart_operations.clear_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    assert select_cart_items_response["selectCartItems"]["id"] is not None
    assert select_cart_items_response["selectCartItems"]["customerId"] == user_response["me"]["id"]
    assert select_cart_items_response["selectCartItems"]["itemsQuantity"] == 1
    assert line_item["selectedForCheckout"] is True


@allure.title("Select all cart items (GraphQL)")
def test_select_all_cart_items(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to select all cart items...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
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
    cart_operations.add_item_to_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        product_id=TEST_PRODUCT_2["id"],
        quantity=1,
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    select_all_cart_items_response = cart_operations.select_all_cart_items(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart_operations.clear_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    assert select_all_cart_items_response["selectAllCartItems"]["id"] is not None
    assert select_all_cart_items_response["selectAllCartItems"]["customerId"] == user_response["me"]["id"]
    assert select_all_cart_items_response["selectAllCartItems"]["itemsQuantity"] == 2
    assert (
        all(item["selectedForCheckout"] for item in select_all_cart_items_response["selectAllCartItems"]["items"])
        is True
    )
