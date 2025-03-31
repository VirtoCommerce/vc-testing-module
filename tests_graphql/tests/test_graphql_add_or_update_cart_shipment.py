import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_address import TEST_CUSTOMER_ADDRESS, TEST_CUSTOMER_ADDRESS_1
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT
from tests_graphql.test_data.test_shipment import TEST_SHIPMENT, TEST_SHIPMENT_1


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
    delivery_address_id = cart["shipments"][0]["deliveryAddress"]["id"]

    # Test teardown
    cart_operations.remove_cart_address(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        address_id=delivery_address_id,
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
    assert cart["shipments"][0]["deliveryAddress"] is not None, "Delivery address is None"
    assert delivery_address_id is not None, "Delivery address ID is None"
    assert cart["shipments"][0]["deliveryAddress"]["city"] == TEST_CUSTOMER_ADDRESS["city"]
    assert cart["shipments"][0]["deliveryAddress"]["countryCode"] == TEST_CUSTOMER_ADDRESS["countryCode"]
    assert cart["shipments"][0]["deliveryAddress"]["countryName"] == TEST_CUSTOMER_ADDRESS["countryName"]
    assert cart["shipments"][0]["deliveryAddress"]["email"] == TEST_CUSTOMER_ADDRESS["email"]
    assert cart["shipments"][0]["deliveryAddress"]["firstName"] == TEST_CUSTOMER_ADDRESS["firstName"]
    assert cart["shipments"][0]["deliveryAddress"]["lastName"] == TEST_CUSTOMER_ADDRESS["lastName"]
    assert cart["shipments"][0]["deliveryAddress"]["line1"] == TEST_CUSTOMER_ADDRESS["line1"]
    assert cart["shipments"][0]["deliveryAddress"]["phone"] == TEST_CUSTOMER_ADDRESS["phone"]
    assert cart["shipments"][0]["deliveryAddress"]["postalCode"] == TEST_CUSTOMER_ADDRESS["postalCode"]
    assert cart["shipments"][0]["deliveryAddress"]["regionId"] == TEST_CUSTOMER_ADDRESS["regionId"]
    assert cart["shipments"][0]["deliveryAddress"]["regionName"] == TEST_CUSTOMER_ADDRESS["regionName"]


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
    delivery_address_id = cart["shipments"][0]["deliveryAddress"]["id"]

    new_address = {
        **TEST_CUSTOMER_ADDRESS_1,
        "id": delivery_address_id,
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

    # Test teardown
    cart_operations.remove_cart_address(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        address_id=delivery_address_id,
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
    assert updated_cart["shipments"][0]["deliveryAddress"] is not None, "Delivery address is None"
    assert delivery_address_id == new_address["id"]
    assert updated_cart["shipments"][0]["deliveryAddress"]["city"] == new_address["city"]
    assert updated_cart["shipments"][0]["deliveryAddress"]["countryCode"] == new_address["countryCode"]
    assert updated_cart["shipments"][0]["deliveryAddress"]["countryName"] == new_address["countryName"]
    assert updated_cart["shipments"][0]["deliveryAddress"]["email"] == new_address["email"]
    assert updated_cart["shipments"][0]["deliveryAddress"]["firstName"] == new_address["firstName"]
    assert updated_cart["shipments"][0]["deliveryAddress"]["lastName"] == new_address["lastName"]
    assert updated_cart["shipments"][0]["deliveryAddress"]["line1"] == new_address["line1"]
    assert updated_cart["shipments"][0]["deliveryAddress"]["phone"] == new_address["phone"]
    assert updated_cart["shipments"][0]["deliveryAddress"]["postalCode"] == new_address["postalCode"]
    assert updated_cart["shipments"][0]["deliveryAddress"]["regionId"] == new_address["regionId"]
    assert updated_cart["shipments"][0]["deliveryAddress"]["regionName"] == new_address["regionName"]


@allure.title("Add cart shipment (GraphQL)")
def test_add_cart_shipment(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to add a cart shipment...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user_response = user_operations.get_me()

    cart_operations = CartOperations(graphql_client)
    cart_response = cart_operations.get_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart = cart_response["cart"]

    ground_shipping_method = next(
        (
            shippingMethod
            for shippingMethod in cart["availableShippingMethods"]
            if shippingMethod["code"] == "FixedRate" and shippingMethod["optionName"] == "Ground"
        )
    )

    shipment = {
        "shipmentMethodCode": ground_shipping_method["code"],
        "shipmentMethodOption": ground_shipping_method["optionName"],
        "price": ground_shipping_method["price"]["amount"],
    }

    add_or_update_cart_shipment_response = cart_operations.add_or_update_cart_shipment(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        shipment=shipment,
    )

    cart_with_shipment = add_or_update_cart_shipment_response["addOrUpdateCartShipment"]
    shipment = cart_with_shipment["shipments"][0]

    # Test teardown
    cart_operations.remove_shipment(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        shipment_id=shipment["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart_operations.remove_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
    )

    assert cart_with_shipment["id"] is not None, "Cart ID is None"
    assert cart["id"] == cart_with_shipment["id"], "Cart ID is not the same"
    assert cart_with_shipment["shipments"] is not None, "Shipments are None"
    assert len(cart_with_shipment["shipments"]) > 0, "Cart has not shipments"
    assert shipment is not None, "Shipment is None"
    assert shipment["id"] is not None, "Shipment ID is None"
    assert shipment["shipmentMethodCode"] == ground_shipping_method["code"]
    assert shipment["shipmentMethodOption"] == ground_shipping_method["optionName"]
    assert shipment["price"]["amount"] == ground_shipping_method["price"]["amount"]


@allure.title("Update cart shipment (GraphQL)")
def test_update_cart_shipment(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to update a cart shipment...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user_response = user_operations.get_me()

    cart_operations = CartOperations(graphql_client)
    cart_response = cart_operations.get_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart = cart_response["cart"]

    ground_shipping_method = next(
        (
            shippingMethod
            for shippingMethod in cart["availableShippingMethods"]
            if shippingMethod["code"] == "FixedRate" and shippingMethod["optionName"] == "Ground"
        )
    )
    air_shipping_method = next(
        (
            shippingMethod
            for shippingMethod in cart["availableShippingMethods"]
            if shippingMethod["code"] == "FixedRate" and shippingMethod["optionName"] == "Air"
        )
    )

    shipment = {
        "shipmentMethodCode": ground_shipping_method["code"],
        "shipmentMethodOption": ground_shipping_method["optionName"],
        "price": ground_shipping_method["price"]["amount"],
    }

    add_or_update_cart_shipment_response = cart_operations.add_or_update_cart_shipment(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        shipment=shipment,
    )

    new_shipment = {
        "id": add_or_update_cart_shipment_response["addOrUpdateCartShipment"]["shipments"][0]["id"],
        "shipmentMethodCode": air_shipping_method["code"],
        "shipmentMethodOption": air_shipping_method["optionName"],
        "price": air_shipping_method["price"]["amount"],
    }

    add_or_update_cart_shipment_response = cart_operations.add_or_update_cart_shipment(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        shipment=new_shipment,
    )

    cart_with_shipment = add_or_update_cart_shipment_response["addOrUpdateCartShipment"]
    shipment = cart_with_shipment["shipments"][0]

    # Test teardown
    cart_operations.remove_shipment(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
        shipment_id=shipment["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart_operations.remove_cart(
        store_id=config["store_id"],
        user_id=user_response["me"]["id"],
    )

    assert cart_with_shipment["id"] is not None, "Cart ID is None"
    assert cart["id"] == cart_with_shipment["id"], "Cart ID is not the same"
    assert cart_with_shipment["shipments"] is not None, "Shipments are None"
    assert len(cart_with_shipment["shipments"]) > 0, "Cart has not shipments"
    assert shipment is not None, "Shipment is None"
    assert shipment["id"] is not None, "Shipment ID is None"
    assert shipment["shipmentMethodCode"] == air_shipping_method["code"]
    assert shipment["shipmentMethodOption"] == air_shipping_method["optionName"]
    assert shipment["price"]["amount"] == air_shipping_method["price"]["amount"]
