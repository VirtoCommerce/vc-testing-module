import os
from typing import Any

import allure
import pytest

from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Add cart billing address (GraphQL)")
def test_add_cart_billing_address(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to add a cart billing address...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]

    user = user_operations.get_me()

    test_address = {
        "id": "test-address-id",
        "addressType": 1,
        "firstName": "Jane",
        "lastName": "Smith",
        "email": "jane.smith@example.com",
        "phone": "+1-650-555-0142",
        "city": "San Mateo",
        "postalCode": "94401",
        "regionId": "CA",
        "regionName": "California",
        "countryCode": "USA",
        "countryName": "United States of America",
        "line1": "1600 Holloway Drive",
    }

    cart = cart_operations.add_or_update_cart_payment(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "payment": {
                "billingAddress": test_address,
            },
        }
    )

    billing_address = cart["payments"][0]["billingAddress"]

    # Test teardown
    cart_operations.remove_cart_address(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "addressId": test_address["id"],
            "currencyCode": currency,
            "cultureName": culture,
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
    assert (
        billing_address["city"] == test_address["city"]
    ), "Billing address city is not the same"
    assert (
        billing_address["countryCode"] == test_address["countryCode"]
    ), "Billing address country code is not the same"
    assert (
        billing_address["countryName"] == test_address["countryName"]
    ), "Billing address country name is not the same"
    assert (
        billing_address["email"] == test_address["email"]
    ), "Billing address email is not the same"
    assert (
        billing_address["firstName"] == test_address["firstName"]
    ), "Billing address first name is not the same"
    assert (
        billing_address["lastName"] == test_address["lastName"]
    ), "Billing address last name is not the same"
    assert (
        billing_address["line1"] == test_address["line1"]
    ), "Billing address line 1 is not the same"
    assert (
        billing_address["phone"] == test_address["phone"]
    ), "Billing address phone is not the same"
    assert (
        billing_address["postalCode"] == test_address["postalCode"]
    ), "Billing address postal code is not the same"
    assert (
        billing_address["regionId"] == test_address["regionId"]
    ), "Billing address region ID is not the same"
    assert (
        billing_address["regionName"] == test_address["regionName"]
    ), "Billing address region name is not the same"


@pytest.mark.graphql
@allure.title("Update cart billing address (GraphQL)")
def test_update_cart_billing_address(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to update a cart billing address...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]

    user = user_operations.get_me()

    test_address = {
        "id": "test-address-id",
        "addressType": 1,
        "firstName": "Jane",
        "lastName": "Smith",
        "email": "jane.smith@example.com",
        "phone": "+1-650-555-0142",
        "city": "San Mateo",
        "postalCode": "94401",
        "regionId": "CA",
        "regionName": "California",
        "countryCode": "USA",
        "countryName": "United States of America",
        "line1": "1600 Holloway Drive",
    }

    cart = cart_operations.add_or_update_cart_payment(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "payment": {
                "billingAddress": test_address,
            },
        }
    )

    billing_address = cart["payments"][0]["billingAddress"]

    new_address = {
        **billing_address,
        "line1": "Some street 123",
        "id": billing_address["id"],
    }

    updated_cart = cart_operations.add_or_update_cart_payment(
        payload={
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
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
            "storeId": config["STORE_ID"],
            "userId": user["id"],
            "addressId": test_address["id"],
            "currencyCode": currency,
            "cultureName": culture,
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
    assert (
        updated_billing_address["city"] == new_address["city"]
    ), "Billing address city is not the same"
    assert (
        updated_billing_address["countryCode"] == new_address["countryCode"]
    ), "Billing address country code is not the same"
    assert (
        updated_billing_address["countryName"] == new_address["countryName"]
    ), "Billing address country name is not the same"
    assert (
        updated_billing_address["email"] == new_address["email"]
    ), "Billing address email is not the same"
    assert (
        updated_billing_address["firstName"] == new_address["firstName"]
    ), "Billing address first name is not the same"
    assert (
        updated_billing_address["lastName"] == new_address["lastName"]
    ), "Billing address last name is not the same"
    assert (
        updated_billing_address["line1"] == new_address["line1"]
    ), "Billing address line 1 is not the same"
    assert (
        updated_billing_address["phone"] == new_address["phone"]
    ), "Billing address phone is not the same"
    assert (
        updated_billing_address["postalCode"] == new_address["postalCode"]
    ), "Billing address postal code is not the same"
    assert (
        updated_billing_address["regionId"] == new_address["regionId"]
    ), "Billing address region ID is not the same"
    assert (
        updated_billing_address["regionName"] == new_address["regionName"]
    ), "Billing address region name is not the same"
