import allure, os, pytest
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from test_data.test_product import TEST_PRODUCT_1, TEST_PRODUCT_2
from fixtures.graphql_client_fixture import GraphQLClient


@pytest.mark.graphql
@allure.title("Select cart items (GraphQL)")
def test_select_cart_items(config: dict, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to select cart items...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    cart_operations.add_items_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "cartItems": [
                {
                    "productId": TEST_PRODUCT_1["id"],
                    "quantity": 1,
                },
                {
                    "productId": TEST_PRODUCT_2["id"],
                    "quantity": 2,
                },
            ],
        }
    )

    cart = cart_operations.unselect_all_cart_items(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
        }
    )

    line_item_to_select = next(item for item in cart["items"] if item["productId"] == TEST_PRODUCT_2["id"])

    updated_cart = cart_operations.select_cart_items(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "lineItemIds": [line_item_to_select["id"]],
        }
    )

    selected_line_item = next(item for item in updated_cart["items"] if item["productId"] == TEST_PRODUCT_2["id"])

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": updated_cart["id"],
            "userId": user["id"],
        }
    )

    assert updated_cart["id"] is not None, "Updated cart ID is missing"
    assert updated_cart["id"] == cart["id"], "Updated cart ID mismatch"
    assert updated_cart["customerId"] == user["id"], "Updated cart customer ID mismatch"
    assert updated_cart["itemsQuantity"] == sum(
        item["quantity"] for item in updated_cart["items"]
    ), "Updated cart items quantity mismatch"
    assert selected_line_item["selectedForCheckout"] is True, "Selected line item is not selected for checkout"
    assert selected_line_item["productId"] == TEST_PRODUCT_2["id"], "Selected line item product ID mismatch"
    assert selected_line_item["quantity"] == 2, "Selected line item quantity mismatch"


@pytest.mark.graphql
@allure.title("Select all cart items (GraphQL)")
def test_select_all_cart_items(config: dict, graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to select all cart items...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    cart_operations.add_items_to_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "cartItems": [
                {
                    "productId": TEST_PRODUCT_1["id"],
                    "quantity": 1,
                },
                {
                    "productId": TEST_PRODUCT_2["id"],
                    "quantity": 2,
                },
            ],
        }
    )

    cart_operations.unselect_all_cart_items(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
        }
    )

    cart = cart_operations.select_all_cart_items(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    assert cart["id"] is not None, "Cart ID is missing"
    assert cart["customerId"] == user["id"], "Cart customer ID mismatch"
    assert cart["itemsQuantity"] == sum(item["quantity"] for item in cart["items"]), "Cart items quantity mismatch"
    assert all(item["selectedForCheckout"] for item in cart["items"]), "All cart items are not selected for checkout"
