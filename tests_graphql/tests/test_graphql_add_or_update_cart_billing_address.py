import os
from typing import Any, Dict

import allure
import pytest

from fixtures.graphql_client_fixture import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Add cart billing address (GraphQL)")
def test_add_cart_billing_address(
    config: Dict[str, Any], dataset: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to add a cart billing address...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]

    user = user_operations.get_me()

    billing_address = dataset["organizations"][0]["addresses"][0]
    billing_address["addressType"] = 1

    cart = cart_operations.add_or_update_cart_payment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "payment": {
                "billingAddress": billing_address,
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
    assert billing_address["id"] is not None, "Billing address ID is None"
    assert (
        billing_address["city"] == billing_address["city"]
    ), "Billing address city is not the same"
    assert (
        billing_address["countryCode"] == billing_address["countryCode"]
    ), "Billing address country code is not the same"
    assert (
        billing_address["countryName"] == billing_address["countryName"]
    ), "Billing address country name is not the same"
    assert (
        billing_address["email"] == billing_address["email"]
    ), "Billing address email is not the same"
    assert (
        billing_address["firstName"] == billing_address["firstName"]
    ), "Billing address first name is not the same"
    assert (
        billing_address["lastName"] == billing_address["lastName"]
    ), "Billing address last name is not the same"
    assert (
        billing_address["line1"] == billing_address["line1"]
    ), "Billing address line 1 is not the same"
    assert (
        billing_address["phone"] == billing_address["phone"]
    ), "Billing address phone is not the same"
    assert (
        billing_address["postalCode"] == billing_address["postalCode"]
    ), "Billing address postal code is not the same"
    assert (
        billing_address["regionId"] == billing_address["regionId"]
    ), "Billing address region ID is not the same"
    assert (
        billing_address["regionName"] == billing_address["regionName"]
    ), "Billing address region name is not the same"


@pytest.mark.graphql
@allure.title("Update cart billing address (GraphQL)")
def test_update_cart_billing_address(
    config: Dict[str, Any], dataset: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to update a cart billing address...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]

    user = user_operations.get_me()

    billing_address = dataset["organizations"][0]["addresses"][0]
    billing_address["addressType"] = 1

    cart = cart_operations.add_or_update_cart_payment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "payment": {
                "billingAddress": billing_address,
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
            "storeId": config["store_id"],
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
            "storeId": config["store_id"],
            "userId": user["id"],
            "addressId": billing_address["id"],
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
    assert updated_billing_address["id"] is not None, "Billing address ID is None"
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
