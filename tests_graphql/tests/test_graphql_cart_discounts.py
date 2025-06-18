import allure, os, pytest
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT_1, TEST_PRODUCT_2, TEST_PRODUCT_3
from tests_graphql.test_data.test_user import TEST_ADMIN_USER


@pytest.mark.graphql
@allure.title("Apply discount for registered user for specific product (GraphQL)")
def test_product_specific_registered_user_cart_discount(config, auth, graphql_client):
    print(f"{os.linesep}Running test to apply discount for specified product for registered user...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    auth.authenticate(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

    user = user_operations.get_user()

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "productId": TEST_PRODUCT_3["id"],
            "quantity": 1,
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "userId": user["id"],
            "cartId": cart["id"],
        }
    )

    auth.clear_token()

    assert user["userName"] == config["username"], "User name is not correct"
    assert cart["discountTotal"]["amount"] == 100, "Discount total is not 50"


@pytest.mark.graphql
@allure.title("Apply discount for specified product (GraphQL)")
def test_product_specific_cart_discount(config, graphql_client):
    print(f"{os.linesep}Running test to apply discount for specified product...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "productId": TEST_PRODUCT_1["id"],
            "quantity": 1,
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "userId": user["id"],
            "cartId": cart["id"],
        }
    )

    assert cart["discountTotal"]["amount"] == 50, "Discount total is not 50"


@allure.title("Apply discount for specified cart subtotal (GraphQL)")
def test_subtotal_specific_cart_discount(config, graphql_client):
    print(f"{os.linesep}Running test to apply discount for specified cart subtotal...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "productId": TEST_PRODUCT_2["id"],
            "quantity": 1,
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "userId": user["id"],
            "cartId": cart["id"],
        }
    )

    assert cart["discountTotal"]["amount"] == 10, "Discount total is not 10"
