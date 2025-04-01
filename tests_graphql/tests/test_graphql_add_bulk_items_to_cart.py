import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT, TEST_PRODUCT_2


@allure.title("Add bulk items to anonymous cart (GraphQL)")
def test_add_bulk_items_to_anonymous_cart(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to add bulk items to anonymous cart...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user_response = user_operations.get_me()

    user = user_response["me"]

    cart_operations = CartOperations(graphql_client)
    add_bulk_items_cart_response = cart_operations.add_bulk_items_to_cart(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        cart_items=[
            {
                "productSku": TEST_PRODUCT["sku"],
                "quantity": 5,
            },
            {
                "productSku": TEST_PRODUCT_2["sku"],
                "quantity": 10,
            },
        ],
    )

    cart = add_bulk_items_cart_response["addBulkItemsCart"]["cart"]
    errors = add_bulk_items_cart_response["addBulkItemsCart"]["errors"]

    duplicate_sku_error = next((error for error in errors if error["errorCode"] == "PRODUCT_DUPLICATE_SKU"), None)

    # Test teardown
    cart_operations.remove_cart(
        store_id=config["store_id"],
        user_id=user["id"],
    )

    assert cart["id"] is not None
    assert cart["customerId"] == user["id"]
    assert len(cart["items"]) > 0
    assert cart["itemsQuantity"] == 10
    assert len(errors) == 1
    assert duplicate_sku_error is not None
    assert duplicate_sku_error["objectId"] == TEST_PRODUCT["sku"]
