import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_address import TEST_CUSTOMER_ADDRESS, TEST_CUSTOMER_ADDRESS_1
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY


@allure.title("Add cart shipment address (GraphQL)")
def test_add_cart_shipment_address(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to add a cart shipment address...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user_response = user_operations.get_me()

    cart_operations = CartOperations(graphql_client)
    add_or_update_cart_shipment_response = cart_operations.add_or_update_cart_shipment(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        shipment={
            "deliveryAddress": TEST_CUSTOMER_ADDRESS,
        },
    )

    cart = add_or_update_cart_shipment_response["addOrUpdateCartShipment"]
    delivery_address = cart["shipments"][0]["deliveryAddress"]

    # Test teardown
    cart_operations.remove_cart_address(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        address_id=delivery_address["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart_operations.remove_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
    )

    assert cart["id"] is not None, "Cart ID is None"
    assert cart["shipments"] is not None, "Shipments are None"
    assert len(cart["shipments"]) > 0, "Cart has not shipments"
    assert delivery_address is not None, "Delivery address is None"
    assert delivery_address["id"] is not None, "Delivery address ID is None"
    assert delivery_address["city"] == TEST_CUSTOMER_ADDRESS["city"]
    assert delivery_address["countryCode"] == TEST_CUSTOMER_ADDRESS["countryCode"]
    assert delivery_address["countryName"] == TEST_CUSTOMER_ADDRESS["countryName"]
    assert delivery_address["email"] == TEST_CUSTOMER_ADDRESS["email"]
    assert delivery_address["firstName"] == TEST_CUSTOMER_ADDRESS["firstName"]
    assert delivery_address["lastName"] == TEST_CUSTOMER_ADDRESS["lastName"]
    assert delivery_address["line1"] == TEST_CUSTOMER_ADDRESS["line1"]
    assert delivery_address["phone"] == TEST_CUSTOMER_ADDRESS["phone"]
    assert delivery_address["postalCode"] == TEST_CUSTOMER_ADDRESS["postalCode"]
    assert delivery_address["regionId"] == TEST_CUSTOMER_ADDRESS["regionId"]
    assert delivery_address["regionName"] == TEST_CUSTOMER_ADDRESS["regionName"]


@allure.title("Update cart shipment address (GraphQL)")
def test_update_cart_shipment_address(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to update a cart shipment address...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user_response = user_operations.get_me()

    cart_operations = CartOperations(graphql_client)
    add_or_update_cart_shipment_response = cart_operations.add_or_update_cart_shipment(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        shipment={
            "deliveryAddress": TEST_CUSTOMER_ADDRESS,
        },
    )

    cart = add_or_update_cart_shipment_response["addOrUpdateCartShipment"]
    delivery_address = cart["shipments"][0]["deliveryAddress"]

    new_address = {
        **TEST_CUSTOMER_ADDRESS_1,
        "id": delivery_address["id"],
    }

    add_or_update_cart_shipment_response = cart_operations.add_or_update_cart_shipment(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        shipment={
            "id": cart["shipments"][0]["id"],
            "deliveryAddress": new_address,
        },
    )

    updated_cart = add_or_update_cart_shipment_response["addOrUpdateCartShipment"]
    updated_delivery_address = updated_cart["shipments"][0]["deliveryAddress"]

    # Test teardown
    cart_operations.remove_cart_address(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        address_id=delivery_address["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart_operations.remove_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
    )

    assert updated_cart["id"] is not None, "Cart ID is None"
    assert updated_cart["shipments"] is not None, "Shipments are None"
    assert len(updated_cart["shipments"]) > 0, "Cart has not shipments"
    assert updated_delivery_address is not None, "Delivery address is None"
    assert updated_delivery_address["id"] is not None, "Delivery address ID is None"
    assert updated_delivery_address["city"] == new_address["city"]
    assert updated_delivery_address["countryCode"] == new_address["countryCode"]
    assert updated_delivery_address["countryName"] == new_address["countryName"]
    assert updated_delivery_address["email"] == new_address["email"]
    assert updated_delivery_address["firstName"] == new_address["firstName"]
    assert updated_delivery_address["lastName"] == new_address["lastName"]
    assert updated_delivery_address["line1"] == new_address["line1"]
    assert updated_delivery_address["phone"] == new_address["phone"]
    assert updated_delivery_address["postalCode"] == new_address["postalCode"]
    assert updated_delivery_address["regionId"] == new_address["regionId"]
    assert updated_delivery_address["regionName"] == new_address["regionName"]
