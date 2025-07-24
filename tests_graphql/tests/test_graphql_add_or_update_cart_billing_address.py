import allure, os, pytest
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_address import TEST_CUSTOMER_ADDRESS_1, TEST_CUSTOMER_ADDRESS_2
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from fixtures.graphql_client_fixture import GraphQLClient
from typing import Dict, Any


@pytest.mark.graphql
@allure.title("Add cart billing address (GraphQL)")
def test_add_cart_billing_address(config: Dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to add a cart billing address...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    cart = cart_operations.add_or_update_cart_payment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "payment": {
                "billingAddress": TEST_CUSTOMER_ADDRESS_1,
            },
        }
    )

    billing_address = cart["payments"][0]["billingAddress"]

    # Test teardown
    cart_operations.remove_cart_address(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "addressId": billing_address["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
        }
    )
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    assert cart["id"] is not None, "Cart ID is None"
    assert cart["payments"] is not None, "Payments are None"
    assert len(cart["payments"]) > 0, "Cart has not payments"
    assert billing_address is not None, "Billing address is None"
    assert billing_address["id"] is not None, "Billing address ID is None"
    assert billing_address["city"] == TEST_CUSTOMER_ADDRESS_1["city"], "Billing address city is not the same"
    assert (
        billing_address["countryCode"] == TEST_CUSTOMER_ADDRESS_1["countryCode"]
    ), "Billing address country code is not the same"
    assert (
        billing_address["countryName"] == TEST_CUSTOMER_ADDRESS_1["countryName"]
    ), "Billing address country name is not the same"
    assert billing_address["email"] == TEST_CUSTOMER_ADDRESS_1["email"], "Billing address email is not the same"
    assert (
        billing_address["firstName"] == TEST_CUSTOMER_ADDRESS_1["firstName"]
    ), "Billing address first name is not the same"
    assert billing_address["lastName"] == TEST_CUSTOMER_ADDRESS_1["lastName"], "Billing address last name is not the same"
    assert billing_address["line1"] == TEST_CUSTOMER_ADDRESS_1["line1"], "Billing address line 1 is not the same"
    assert billing_address["phone"] == TEST_CUSTOMER_ADDRESS_1["phone"], "Billing address phone is not the same"
    assert (
        billing_address["postalCode"] == TEST_CUSTOMER_ADDRESS_1["postalCode"]
    ), "Billing address postal code is not the same"
    assert billing_address["regionId"] == TEST_CUSTOMER_ADDRESS_1["regionId"], "Billing address region ID is not the same"
    assert (
        billing_address["regionName"] == TEST_CUSTOMER_ADDRESS_1["regionName"]
    ), "Billing address region name is not the same"


@pytest.mark.graphql
@allure.title("Update cart billing address (GraphQL)")
def test_update_cart_billing_address(config: Dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to update a cart billing address...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    cart = cart_operations.add_or_update_cart_payment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "payment": {
                "billingAddress": TEST_CUSTOMER_ADDRESS_1,
            },
        }
    )

    billing_address = cart["payments"][0]["billingAddress"]

    new_address = {
        **TEST_CUSTOMER_ADDRESS_2,
        "id": billing_address["id"],
    }

    updated_cart = cart_operations.add_or_update_cart_payment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "payment": {
                "id": cart["payments"][0]["id"],
                "billingAddress": new_address,
            },
        }
    )

    updated_billing_address = updated_cart["payments"][0]["billingAddress"]

    # Test teardown
    cart_operations.remove_cart_address(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "addressId": billing_address["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
        }
    )
    cart_operations.remove_cart(
        payload={
            "cartId": cart["id"],
            "userId": user["id"],
        }
    )

    assert updated_cart["id"] is not None, "Cart ID is None"
    assert updated_cart["payments"] is not None, "Payments are None"
    assert len(updated_cart["payments"]) > 0, "Cart has not payments"
    assert updated_billing_address is not None, "Billing address is None"
    assert updated_billing_address["id"] is not None, "Billing address ID is None"
    assert updated_billing_address["city"] == new_address["city"], "Billing address city is not the same"
    assert (
        updated_billing_address["countryCode"] == new_address["countryCode"]
    ), "Billing address country code is not the same"
    assert (
        updated_billing_address["countryName"] == new_address["countryName"]
    ), "Billing address country name is not the same"
    assert updated_billing_address["email"] == new_address["email"], "Billing address email is not the same"
    assert (
        updated_billing_address["firstName"] == new_address["firstName"]
    ), "Billing address first name is not the same"
    assert updated_billing_address["lastName"] == new_address["lastName"], "Billing address last name is not the same"
    assert updated_billing_address["line1"] == new_address["line1"], "Billing address line 1 is not the same"
    assert updated_billing_address["phone"] == new_address["phone"], "Billing address phone is not the same"
    assert (
        updated_billing_address["postalCode"] == new_address["postalCode"]
    ), "Billing address postal code is not the same"
    assert updated_billing_address["regionId"] == new_address["regionId"], "Billing address region ID is not the same"
    assert (
        updated_billing_address["regionName"] == new_address["regionName"]
    ), "Billing address region name is not the same"
