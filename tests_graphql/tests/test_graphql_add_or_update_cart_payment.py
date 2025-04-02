import allure
import os
from tests_graphql.operations.cart.cart_operations import CartOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY


@allure.title("Add cart payment (GraphQL)")
def test_add_cart_payment(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to add a cart payment...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user = user_operations.get_me()["me"]

    cart_operations = CartOperations(graphql_client)
    cart = cart_operations.get_cart(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )["cart"]

    manual_payment_method = next(
        (
            paymentMethod
            for paymentMethod in cart["availablePaymentMethods"]
            if paymentMethod["code"] == "DefaultManualPaymentMethod"
        )
    )

    payment = {
        "paymentGatewayCode": manual_payment_method["code"],
        "price": manual_payment_method["price"]["amount"],
    }

    cart_with_payment = cart_operations.add_or_update_cart_payment(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        payment=payment,
    )["addOrUpdateCartPayment"]

    updated_payment = cart_with_payment["payments"][0]

    # Test teardown
    cart_operations.clear_payments(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart_operations.remove_cart(
        cart_id=cart_with_payment["id"],
        user_id=user["id"],
    )

    assert cart_with_payment["id"] is not None, "Cart ID is None"
    assert cart["id"] == cart_with_payment["id"], "Cart ID is not the same"
    assert cart_with_payment["payments"] is not None, "Payments are None"
    assert len(cart_with_payment["payments"]) > 0, "Cart has not payments"
    assert updated_payment is not None, "Payment is None"
    assert updated_payment["id"] is not None, "Payment ID is None"
    assert updated_payment["paymentGatewayCode"] == manual_payment_method["code"]
    assert updated_payment["price"]["amount"] == manual_payment_method["price"]["amount"]


@allure.title("Update cart payment (GraphQL)")
def test_update_cart_payment(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to update a cart payment...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    user = user_operations.get_me()["me"]

    cart_operations = CartOperations(graphql_client)
    cart = cart_operations.get_cart(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )["cart"]

    manual_payment_method = next(
        (
            paymentMethod
            for paymentMethod in cart["availablePaymentMethods"]
            if paymentMethod["code"] == "DefaultManualPaymentMethod"
        )
    )

    authorize_net_payment_method = next(
        (
            paymentMethod
            for paymentMethod in cart["availablePaymentMethods"]
            if paymentMethod["code"] == "AuthorizeNetPaymentMethod"
        )
    )

    payment = {
        "paymentGatewayCode": manual_payment_method["code"],
        "price": authorize_net_payment_method["price"]["amount"],
    }

    cart_with_payment = cart_operations.add_or_update_cart_payment(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        payment=payment,
    )["addOrUpdateCartPayment"]

    new_payment = {
        "id": cart_with_payment["payments"][0]["id"],
        "paymentGatewayCode": authorize_net_payment_method["code"],
        "price": authorize_net_payment_method["price"]["amount"],
    }

    updated_cart = cart_operations.add_or_update_cart_payment(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        payment=new_payment,
    )["addOrUpdateCartPayment"]

    updated_payment = updated_cart["payments"][0]

    # Test teardown
    cart_operations.clear_payments(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
    )

    cart_operations.remove_cart(
        cart_id=updated_cart["id"],
        user_id=user["id"],
    )

    assert cart_with_payment["id"] is not None, "Cart ID is None"
    assert cart["id"] == cart_with_payment["id"], "Cart ID is not the same"
    assert cart_with_payment["payments"] is not None, "Payments are None"
    assert len(cart_with_payment["payments"]) > 0, "Cart has not payments"
    assert updated_payment is not None, "Payment is None"
    assert updated_payment["id"] is not None, "Payment ID is None"
    assert updated_payment["paymentGatewayCode"] == authorize_net_payment_method["code"]
    assert updated_payment["price"]["amount"] == authorize_net_payment_method["price"]["amount"]
