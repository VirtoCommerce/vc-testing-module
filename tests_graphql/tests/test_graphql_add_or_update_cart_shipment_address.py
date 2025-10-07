import os
from typing import Any

import allure
import pytest

from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Add cart shipment address (GraphQL)")
def test_add_cart_shipment_address(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to add a cart shipment address...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]

    user = user_operations.get_me()

    test_address = {
        "id": "test-address-id",
        "addressType": 2,
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

    cart = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "shipment": {
                "deliveryAddress": test_address,
            },
        }
    )

    delivery_address = cart["shipments"][0]["deliveryAddress"]

    # Test teardown
    cart_operations.remove_cart_address(
        payload={
            "storeId": config["store_id"],
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
    assert cart["shipments"] is not None, "Shipments are None"
    assert len(cart["shipments"]) > 0, "Cart has not shipments"
    assert delivery_address is not None, "Delivery address is None"
    assert (
        delivery_address["city"] == test_address["city"]
    ), "Delivery address city is not the same"
    assert (
        delivery_address["countryCode"] == test_address["countryCode"]
    ), "Delivery address country code is not the same"
    assert (
        delivery_address["countryName"] == test_address["countryName"]
    ), "Delivery address country name is not the same"
    assert (
        delivery_address["email"] == test_address["email"]
    ), "Delivery address email is not the same"
    assert (
        delivery_address["firstName"] == test_address["firstName"]
    ), "Delivery address first name is not the same"
    assert (
        delivery_address["lastName"] == test_address["lastName"]
    ), "Delivery address last name is not the same"
    assert (
        delivery_address["line1"] == test_address["line1"]
    ), "Delivery address line 1 is not the same"
    assert (
        delivery_address["phone"] == test_address["phone"]
    ), "Delivery address phone is not the same"
    assert (
        delivery_address["postalCode"] == test_address["postalCode"]
    ), "Delivery address postal code is not the same"
    assert (
        delivery_address["regionId"] == test_address["regionId"]
    ), "Delivery address region ID is not the same"
    assert (
        delivery_address["regionName"] == test_address["regionName"]
    ), "Delivery address region name is not the same"


@pytest.mark.graphql
@allure.title("Update cart shipment address (GraphQL)")
def test_update_cart_shipment_address(
    config: dict[str, Any], dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to update a cart shipment address...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]

    user = user_operations.get_me()

    test_address = {
        "id": "test-address-id",
        "addressType": 2,
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

    cart = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "shipment": {
                "deliveryAddress": test_address,
            },
        }
    )

    delivery_address = cart["shipments"][0]["deliveryAddress"]

    new_address = {
        **test_address,
        "line1": "Some street 123",
        "id": delivery_address["id"],
    }

    updated_cart = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": currency,
            "cultureName": culture,
            "shipment": {
                "id": cart["shipments"][0]["id"],
                "deliveryAddress": new_address,
            },
        }
    )

    updated_delivery_address = updated_cart["shipments"][0]["deliveryAddress"]

    # Test teardown
    cart_operations.remove_cart_address(
        payload={
            "storeId": config["store_id"],
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
    assert updated_cart["shipments"] is not None, "Shipments are None"
    assert len(updated_cart["shipments"]) > 0, "Cart has not shipments"
    assert updated_delivery_address is not None, "Delivery address is None"
    assert (
        updated_delivery_address["city"] == new_address["city"]
    ), "Delivery address city is not the same"
    assert (
        updated_delivery_address["countryCode"] == new_address["countryCode"]
    ), "Delivery address country code is not the same"
    assert (
        updated_delivery_address["countryName"] == new_address["countryName"]
    ), "Delivery address country name is not the same"
    assert (
        updated_delivery_address["email"] == new_address["email"]
    ), "Delivery address email is not the same"
    assert (
        updated_delivery_address["firstName"] == new_address["firstName"]
    ), "Delivery address first name is not the same"
    assert (
        updated_delivery_address["lastName"] == new_address["lastName"]
    ), "Delivery address last name is not the same"
    assert (
        updated_delivery_address["line1"] == new_address["line1"]
    ), "Delivery address line 1 is not the same"
    assert (
        updated_delivery_address["phone"] == new_address["phone"]
    ), "Delivery address phone is not the same"
    assert (
        updated_delivery_address["postalCode"] == new_address["postalCode"]
    ), "Delivery address postal code is not the same"
    assert (
        updated_delivery_address["regionId"] == new_address["regionId"]
    ), "Delivery address region ID is not the same"
    assert (
        updated_delivery_address["regionName"] == new_address["regionName"]
    ), "Delivery address region name is not the same"
