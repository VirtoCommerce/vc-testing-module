import allure, os
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT_1


@allure.title("Change cart item quantity (GraphQL)")
def test_cart_item_quantity(config, graphql_client):
    print(f"{os.linesep}Running test to change cart item quantity...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    cart = cart_operations.add_item_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "productId": TEST_PRODUCT_1["id"],
            "quantity": 1,
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
        }
    )

    line_item = cart["items"][0]

    updated_cart = cart_operations.change_cart_item_quantity(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "lineItemId": line_item["id"],
            "quantity": 10,
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": updated_cart["id"],
            "userId": user["id"],
        }
    )

    assert updated_cart["id"] is not None, "Cart ID is None"
    assert updated_cart["customerId"] == user["id"], "Customer ID is not the same"
    assert updated_cart["itemsQuantity"] == 10, "Items quantity is not the same"
