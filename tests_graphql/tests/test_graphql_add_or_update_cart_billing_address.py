import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_address import TEST_CUSTOMER_ADDRESS, TEST_CUSTOMER_ADDRESS_1
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY


@allure.title("Add cart billing address (GraphQL)")
def test_add_cart_billing_address(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to add a cart billing address...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user = user_operations.get_me()["me"]

    cart_operations = CartOperations(graphql_client)
    cart = cart_operations.add_or_update_cart_payment(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        payment={
            "billingAddress": TEST_CUSTOMER_ADDRESS,
        },
    )["addOrUpdateCartPayment"]

    billing_address = cart["payments"][0]["billingAddress"]

    # Test teardown
    cart_operations.remove_cart_address(
        store_id=config["store_id"],
        user_id=user["id"],
        address_id=billing_address["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart_operations.remove_cart(
        cart_id=cart["id"],
        user_id=user["id"],
    )

    assert cart["id"] is not None, "Cart ID is None"
    assert cart["payments"] is not None, "Payments are None"
    assert len(cart["payments"]) > 0, "Cart has not payments"
    assert billing_address is not None, "Billing address is None"
    assert billing_address["id"] is not None, "Billing address ID is None"
    assert billing_address["city"] == TEST_CUSTOMER_ADDRESS["city"]
    assert billing_address["countryCode"] == TEST_CUSTOMER_ADDRESS["countryCode"]
    assert billing_address["countryName"] == TEST_CUSTOMER_ADDRESS["countryName"]
    assert billing_address["email"] == TEST_CUSTOMER_ADDRESS["email"]
    assert billing_address["firstName"] == TEST_CUSTOMER_ADDRESS["firstName"]
    assert billing_address["lastName"] == TEST_CUSTOMER_ADDRESS["lastName"]
    assert billing_address["line1"] == TEST_CUSTOMER_ADDRESS["line1"]
    assert billing_address["phone"] == TEST_CUSTOMER_ADDRESS["phone"]
    assert billing_address["postalCode"] == TEST_CUSTOMER_ADDRESS["postalCode"]
    assert billing_address["regionId"] == TEST_CUSTOMER_ADDRESS["regionId"]
    assert billing_address["regionName"] == TEST_CUSTOMER_ADDRESS["regionName"]


@allure.title("Update cart billing address (GraphQL)")
def test_update_cart_billing_address(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to update a cart billing address...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user = user_operations.get_me()["me"]

    cart_operations = CartOperations(graphql_client)
    cart = cart_operations.add_or_update_cart_payment(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        payment={
            "billingAddress": TEST_CUSTOMER_ADDRESS,
        },
    )["addOrUpdateCartPayment"]

    billing_address = cart["payments"][0]["billingAddress"]

    new_address = {
        **TEST_CUSTOMER_ADDRESS_1,
        "id": billing_address["id"],
    }

    updated_cart = cart_operations.add_or_update_cart_payment(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        payment={
            "id": cart["payments"][0]["id"],
            "billingAddress": new_address,
        },
    )["addOrUpdateCartPayment"]

    updated_billing_address = updated_cart["payments"][0]["billingAddress"]

    # Test teardown
    cart_operations.remove_cart_address(
        store_id=config["store_id"],
        user_id=user["id"],
        address_id=billing_address["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart_operations.remove_cart(
        cart_id=cart["id"],
        user_id=user["id"],
    )

    assert updated_cart["id"] is not None, "Cart ID is None"
    assert updated_cart["payments"] is not None, "Payments are None"
    assert len(updated_cart["payments"]) > 0, "Cart has not payments"
    assert updated_billing_address is not None, "Billing address is None"
    assert updated_billing_address["id"] is not None, "Billing address ID is None"
    assert updated_billing_address["city"] == new_address["city"]
    assert updated_billing_address["countryCode"] == new_address["countryCode"]
    assert updated_billing_address["countryName"] == new_address["countryName"]
    assert updated_billing_address["email"] == new_address["email"]
    assert updated_billing_address["firstName"] == new_address["firstName"]
    assert updated_billing_address["lastName"] == new_address["lastName"]
    assert updated_billing_address["line1"] == new_address["line1"]
    assert updated_billing_address["phone"] == new_address["phone"]
    assert updated_billing_address["postalCode"] == new_address["postalCode"]
    assert updated_billing_address["regionId"] == new_address["regionId"]
    assert updated_billing_address["regionName"] == new_address["regionName"]
