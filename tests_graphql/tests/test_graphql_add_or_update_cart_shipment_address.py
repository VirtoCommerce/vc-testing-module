import allure, os, pytest
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from test_data.test_address import TEST_CUSTOMER_ADDRESS_1, TEST_CUSTOMER_ADDRESS_2
from test_data.test_culture import TEST_CULTURE
from test_data.test_currency import TEST_CURRENCY
from fixtures.graphql_client_fixture import GraphQLClient
from typing import Dict, Any


@pytest.mark.graphql
@allure.title("Add cart shipment address (GraphQL)")
def test_add_cart_shipment_address(config: Dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to add a cart shipment address...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    cart = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "shipment": {
                "deliveryAddress": TEST_CUSTOMER_ADDRESS_1,
            },
        }
    )

    delivery_address = cart["shipments"][0]["deliveryAddress"]

    # Test teardown
    cart_operations.remove_cart_address(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "addressId": delivery_address["id"],
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
    assert cart["shipments"] is not None, "Shipments are None"
    assert len(cart["shipments"]) > 0, "Cart has not shipments"
    assert delivery_address is not None, "Delivery address is None"
    assert delivery_address["id"] is not None, "Delivery address ID is None"
    assert delivery_address["city"] == TEST_CUSTOMER_ADDRESS_1["city"], "Delivery address city is not the same"
    assert (
        delivery_address["countryCode"] == TEST_CUSTOMER_ADDRESS_1["countryCode"]
    ), "Delivery address country code is not the same"
    assert (
        delivery_address["countryName"] == TEST_CUSTOMER_ADDRESS_1["countryName"]
    ), "Delivery address country name is not the same"
    assert delivery_address["email"] == TEST_CUSTOMER_ADDRESS_1["email"], "Delivery address email is not the same"
    assert (
        delivery_address["firstName"] == TEST_CUSTOMER_ADDRESS_1["firstName"]
    ), "Delivery address first name is not the same"
    assert (
        delivery_address["lastName"] == TEST_CUSTOMER_ADDRESS_1["lastName"]
    ), "Delivery address last name is not the same"
    assert delivery_address["line1"] == TEST_CUSTOMER_ADDRESS_1["line1"], "Delivery address line 1 is not the same"
    assert delivery_address["phone"] == TEST_CUSTOMER_ADDRESS_1["phone"], "Delivery address phone is not the same"
    assert (
        delivery_address["postalCode"] == TEST_CUSTOMER_ADDRESS_1["postalCode"]
    ), "Delivery address postal code is not the same"
    assert (
        delivery_address["regionId"] == TEST_CUSTOMER_ADDRESS_1["regionId"]
    ), "Delivery address region ID is not the same"
    assert (
        delivery_address["regionName"] == TEST_CUSTOMER_ADDRESS_1["regionName"]
    ), "Delivery address region name is not the same"


@pytest.mark.graphql
@allure.title("Update cart shipment address (GraphQL)")
def test_update_cart_shipment_address(config: Dict[str, Any], graphql_client: GraphQLClient):
    print(f"{os.linesep}Running test to update a cart shipment address...", end=" ")

    user_operations = UserOperations(graphql_client)
    cart_operations = CartOperations(graphql_client)

    user = user_operations.get_user()

    cart = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
            "shipment": {
                "deliveryAddress": TEST_CUSTOMER_ADDRESS_1,
            },
        }
    )

    delivery_address = cart["shipments"][0]["deliveryAddress"]

    new_address = {
        **TEST_CUSTOMER_ADDRESS_2,
        "id": delivery_address["id"],
    }

    updated_cart = cart_operations.add_or_update_cart_shipment(
        payload={
            "storeId": config["store_id"],
            "userId": user["id"],
            "currencyCode": TEST_CURRENCY["USD"],
            "cultureName": TEST_CULTURE["en-US"],
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
            "addressId": delivery_address["id"],
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
    assert updated_cart["shipments"] is not None, "Shipments are None"
    assert len(updated_cart["shipments"]) > 0, "Cart has not shipments"
    assert updated_delivery_address is not None, "Delivery address is None"
    assert updated_delivery_address["id"] is not None, "Delivery address ID is None"
    assert updated_delivery_address["city"] == new_address["city"], "Delivery address city is not the same"
    assert (
        updated_delivery_address["countryCode"] == new_address["countryCode"]
    ), "Delivery address country code is not the same"
    assert (
        updated_delivery_address["countryName"] == new_address["countryName"]
    ), "Delivery address country name is not the same"
    assert updated_delivery_address["email"] == new_address["email"], "Delivery address email is not the same"
    assert (
        updated_delivery_address["firstName"] == new_address["firstName"]
    ), "Delivery address first name is not the same"
    assert updated_delivery_address["lastName"] == new_address["lastName"], "Delivery address last name is not the same"
    assert updated_delivery_address["line1"] == new_address["line1"], "Delivery address line 1 is not the same"
    assert updated_delivery_address["phone"] == new_address["phone"], "Delivery address phone is not the same"
    assert (
        updated_delivery_address["postalCode"] == new_address["postalCode"]
    ), "Delivery address postal code is not the same"
    assert updated_delivery_address["regionId"] == new_address["regionId"], "Delivery address region ID is not the same"
    assert (
        updated_delivery_address["regionName"] == new_address["regionName"]
    ), "Delivery address region name is not the same"
