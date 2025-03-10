import allure
import pytest
from graphql_requests.get_full_cart.get_full_cart_request import GetFullCartRequest
from graphql_requests.clear_cart.clear_cart_request import ClearCartRequest


@pytest.fixture(autouse=True)
@allure.title("Clear cart if not empty before and after test")
def clear_cart_if_not_empty(graphql_client, user_context):
    # Before test
    get_cart = GetFullCartRequest(graphql_client)
    cart = get_cart.execute(user_context["me"]["id"])

    if cart["cart"]["itemsQuantity"] > 0:
        clear_cart = ClearCartRequest(graphql_client)
        clear_cart.execute(user_context["me"]["id"], cart["cart"]["id"])

    yield  # This is where the test runs

    # After test
    cart = get_cart.execute(user_context["me"]["id"])
    if cart["cart"]["itemsQuantity"] > 0:
        clear_cart = ClearCartRequest(graphql_client)
        clear_cart.execute(user_context["me"]["id"], cart["cart"]["id"])
