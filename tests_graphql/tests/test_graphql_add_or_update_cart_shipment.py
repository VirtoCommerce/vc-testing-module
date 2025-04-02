import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY


@allure.title("Add cart shipment (GraphQL)")
def test_add_cart_shipment(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to add a cart shipment...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user = user_operations.get_me()["me"]

    cart_operations = CartOperations(graphql_client)
    cart = cart_operations.get_cart(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )["cart"]

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

    cart_with_shipment = cart_operations.add_or_update_cart_shipment(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        shipment=shipment,
    )["addOrUpdateCartShipment"]

    updated_shipment = cart_with_shipment["shipments"][0]

    # Test teardown
    cart_operations.remove_shipment(
        store_id=config["store_id"],
        user_id=user["id"],
        shipment_id=updated_shipment["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart_operations.remove_cart(
        cart_id=cart_with_shipment["id"],
        user_id=user["id"],
    )

    assert cart_with_shipment["id"] is not None, "Cart ID is None"
    assert cart["id"] == cart_with_shipment["id"], "Cart ID is not the same"
    assert cart_with_shipment["shipments"] is not None, "Shipments are None"
    assert len(cart_with_shipment["shipments"]) > 0, "Cart has not shipments"
    assert updated_shipment is not None, "Shipment is None"
    assert updated_shipment["id"] is not None, "Shipment ID is None"
    assert updated_shipment["shipmentMethodCode"] == ground_shipping_method["code"]
    assert updated_shipment["shipmentMethodOption"] == ground_shipping_method["optionName"]
    assert updated_shipment["price"]["amount"] == ground_shipping_method["price"]["amount"]


@allure.title("Update cart shipment (GraphQL)")
def test_update_cart_shipment(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to update a cart shipment...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user = user_operations.get_me()["me"]

    cart_operations = CartOperations(graphql_client)
    cart = cart_operations.get_cart(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )["cart"]

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
        user_id=user["id"],
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

    cart_with_shipment = cart_operations.add_or_update_cart_shipment(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        shipment=new_shipment,
    )["addOrUpdateCartShipment"]

    updated_shipment = cart_with_shipment["shipments"][0]

    # Test teardown
    cart_operations.remove_shipment(
        store_id=config["store_id"],
        user_id=user["id"],
        shipment_id=updated_shipment["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart_operations.remove_cart(
        cart_id=cart_with_shipment["id"],
        user_id=user["id"],
    )

    assert cart_with_shipment["id"] is not None, "Cart ID is None"
    assert cart["id"] == cart_with_shipment["id"], "Cart ID is not the same"
    assert cart_with_shipment["shipments"] is not None, "Shipments are None"
    assert len(cart_with_shipment["shipments"]) > 0, "Cart has not shipments"
    assert updated_shipment is not None, "Shipment is None"
    assert updated_shipment["id"] is not None, "Shipment ID is None"
    assert updated_shipment["shipmentMethodCode"] == air_shipping_method["code"]
    assert updated_shipment["shipmentMethodOption"] == air_shipping_method["optionName"]
    assert updated_shipment["price"]["amount"] == air_shipping_method["price"]["amount"]
