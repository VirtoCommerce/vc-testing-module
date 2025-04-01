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

    user = user_response["me"]

    cart_operations = CartOperations(graphql_client)
    cart_operations.add_items_to_cart(
        store_id=config["store_id"],
        user_id=user["id"],
        cart_items=[
            {
                "productId": TEST_PRODUCT["id"],
                "quantity": 1,
            },
            {
                "productId": TEST_PRODUCT_2["id"],
                "quantity": 2,
            },
        ],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    unselect_all_cart_items_response = cart_operations.unselect_all_cart_items(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart = unselect_all_cart_items_response["unSelectAllCartItems"]
    line_item_to_select = next(item for item in cart["items"] if item["productId"] == TEST_PRODUCT_2["id"])

    select_cart_items_response = cart_operations.select_cart_items(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        line_item_ids=[line_item_to_select["id"]],
    )

    updated_cart = select_cart_items_response["selectCartItems"]
    selected_line_item = next(item for item in updated_cart["items"] if item["productId"] == TEST_PRODUCT_2["id"])

    # Test teardown
    cart_operations.remove_cart(
        store_id=config["store_id"],
        user_id=user["id"],
    )

    assert updated_cart["id"] is not None
    assert updated_cart["id"] == cart["id"]
    assert updated_cart["customerId"] == user["id"]
    assert updated_cart["itemsQuantity"] == sum(item["quantity"] for item in updated_cart["items"])
    assert selected_line_item["selectedForCheckout"] is True
    assert selected_line_item["productId"] == TEST_PRODUCT_2["id"]
    assert selected_line_item["quantity"] == 2


@allure.title("Select all cart items (GraphQL)")
def test_select_all_cart_items(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to select all cart items...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user_response = user_operations.get_me()

    user = user_response["me"]

    cart_operations = CartOperations(graphql_client)
    cart_operations.add_items_to_cart(
        store_id=config["store_id"],
        user_id=user["id"],
        cart_items=[
            {
                "productId": TEST_PRODUCT["id"],
                "quantity": 1,
            },
            {
                "productId": TEST_PRODUCT_2["id"],
                "quantity": 2,
            },
        ],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart_operations.unselect_all_cart_items(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    select_all_cart_items_response = cart_operations.select_all_cart_items(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart = select_all_cart_items_response["selectAllCartItems"]

    # Test teardown
    cart_operations.remove_cart(
        store_id=config["store_id"],
        user_id=user["id"],
    )

    assert cart["id"] is not None
    assert cart["customerId"] == user["id"]
    assert cart["itemsQuantity"] == sum(item["quantity"] for item in cart["items"])
    assert all(item["selectedForCheckout"] for item in cart["items"]) is True
