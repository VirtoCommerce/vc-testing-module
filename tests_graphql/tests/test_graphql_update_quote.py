import allure, os
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.quote.quote_operations import QuoteOperations
from tests_graphql.test_data.test_user import TEST_PERMANENT_USER
from tests_graphql.test_data.test_product import TEST_PRODUCT_1
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_address import TEST_CUSTOMER_ADDRESS


@allure.title("Change quote item quantity (GraphQL)")
def test_change_quote_item_quantity(config, user_service, graphql_client):
    print(f"{os.linesep}Running test to change quote item quantity...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

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

    quote_operations.change_quote_item_quantity(
        payload={
            "quoteId": quote["id"],
            "lineItemId": quote["items"][0]["id"],
            "quantity": 2,
        }
    )

    updated_quote = quote_operations.get_quote(
        store_id=config["store_id"],
        user_id=user["id"],
        id=quote["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    # Test teardown
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    user_service.sign_out()

    assert updated_quote["id"] == quote["id"], "Quote ID is not the same"
    assert updated_quote["items"][0]["selectedTierPrice"]["quantity"] == 2, "Quote item quantity is not the same"


@allure.title("Change quote comment (GraphQL)")
def test_change_quote_comment(config, user_service, graphql_client):
    print(f"{os.linesep}Running test to change quote comment...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

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

    updated_quote = quote_operations.change_quote_comment(
        payload={
            "quoteId": quote["id"],
            "comment": "Updated comment",
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

    assert updated_quote["id"] == quote["id"], "Quote ID is not the same"
    assert updated_quote["comment"] == "Updated comment", "Quote comment is not the same"


@allure.title("Remove quote shipping and billing addresses (GraphQL)")
def test_change_quote_shipping_and_billing_addresses(config, user_service, graphql_client):
    print(f"{os.linesep}Running test to change quote shipping and billing addresses...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

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

    updated_quote = quote_operations.change_quote_addresses(
        payload={
            "quoteId": quote["id"],
            "addresses": [
                {**TEST_CUSTOMER_ADDRESS, "addressType": 1},
                {**TEST_CUSTOMER_ADDRESS, "addressType": 2},
            ],
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

    assert updated_quote["id"] == quote["id"], "Quote ID is not the same"
    assert len(updated_quote["addresses"]) == 2, "Number of addresses is not the same"
    assert any(
        addr["addressType"] == 1 for addr in updated_quote["addresses"]
    ), "Quote has no shipping address (type 1)"
    assert any(addr["addressType"] == 2 for addr in updated_quote["addresses"]), "Quote has no billing address (type 2)"


@allure.title("Remove quote item (GraphQL)")
def test_remove_quote_item(config, user_service, graphql_client):
    print(f"{os.linesep}Running test to remove quote item...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

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

    updated_quote = quote_operations.remove_quote_item(
        payload={
            "quoteId": quote["id"],
            "lineItemId": quote["items"][0]["id"],
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

    assert updated_quote["id"] == quote["id"], "Quote ID is not the same"
    assert len(updated_quote["items"]) == 0, "Quote has items"


@allure.title("Submit quote request (GraphQL)")
def test_submit_quote_request(config, user_service, graphql_client):
    print(f"{os.linesep}Running test to submit quote request...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)
    quote_operations = QuoteOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

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

    updated_quote = quote_operations.submit_quote(
        payload={
            "quoteId": quote["id"],
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

    assert updated_quote["id"] == quote["id"], "Quote ID is not the same"
    assert updated_quote["status"] == "Processing", "Quote status is not the same"
