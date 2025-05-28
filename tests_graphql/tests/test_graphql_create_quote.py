import allure, os
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.quote.quote_operations import QuoteOperations
from tests_graphql.test_data.test_user import TEST_ADMIN_USER
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_product import TEST_PRODUCT_1


@allure.title("Create empty quote from cart (GraphQL)")
def test_create_empty_quote_from_cart(config, user_service, graphql_client):
    print(f"{os.linesep}Running test to create empty quote from cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    user_service.sign_in(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

    user = user_operations.get_user()

    cart = cart_operations.get_cart(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    quote = quote_operations.create_quote_from_cart(
        payload={
            "cartId": cart["id"],
            "comment": "Test comment",
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    user_service.sign_out()

    assert quote["id"] is not None, "Quote ID is None"
    assert quote["number"] is not None, "Quote number is None"
    assert quote["status"] == "Draft", "Quote status is not Draft"
    assert quote["storeId"] == config["store_id"], "Quote store ID is not correct"
    assert quote["customerId"] == user["id"], "Quote customer ID is not correct"
    assert quote["comment"] == "Test comment", "Quote comment is not correct"
    assert len(quote["items"]) == 0, "Quote items are not empty"


def test_create_quote_with_items_from_cart(config, user_service, graphql_client):
    print(f"{os.linesep}Running test to create quote with items from cart...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    user_service.sign_in(TEST_ADMIN_USER["username"], TEST_ADMIN_USER["password"])

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

    quote = quote_operations.create_quote_from_cart(
        payload={
            "cartId": cart["id"],
            "comment": "Test comment",
        }
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    user_service.sign_out()

    assert quote["id"] is not None, "Quote ID is None"
    assert quote["number"] is not None, "Quote number is None"
    assert quote["status"] == "Draft", "Quote status is not Draft"
    assert quote["storeId"] == config["store_id"], "Quote store ID is not correct"
    assert quote["customerId"] == user["id"], "Quote customer ID is not correct"
    assert quote["comment"] == "Test comment", "Quote comment is not correct"
    assert len(quote["items"]) > 0, "Quote items are empty"
    assert quote["items"][0]["productId"] == TEST_PRODUCT_1["id"], "Quote item product ID is not correct"
