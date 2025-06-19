import allure, os, pytest
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT_1, TEST_PRODUCT_2
from tests_graphql.test_data.test_user import TEST_ADMIN_USER


@pytest.mark.graphql
@allure.title("Merge carts (GraphQL)")
def test_merge_carts(config, auth, graphql_client):
    print(f"{os.linesep}Running test to merge carts...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    anonymous_user = user_operations.get_user()

    anonymous_cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": anonymous_user["id"],
            "productId": TEST_PRODUCT_1["id"],
            "quantity": 1,
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
        }
    )

    auth.authenticate(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

    registered_user = user_operations.get_user()

    registered_user_cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": registered_user["id"],
            "productId": TEST_PRODUCT_2["id"],
            "quantity": 2,
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
        }
    )

    merged_cart = cart_operations.merge_cart(
        payload={
            "storeId": config["store_id"],
            "userId": registered_user["id"],
            "secondCartId": anonymous_cart["id"],
            "cultureName": TEST_CULTURE["en-US"],
            "currencyCode": TEST_CURRENCY["USD"],
            "deleteAfterMerge": True,
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": merged_cart["id"],
            "userId": registered_user["id"],
        }
    )

    auth.clear_token()

    assert merged_cart["id"] is not None, "Merged cart ID is missing"
    assert merged_cart["id"] == registered_user_cart["id"], "Merged cart ID mismatch"
    assert merged_cart["itemsQuantity"] == 3, "Merged cart items quantity mismatch"
