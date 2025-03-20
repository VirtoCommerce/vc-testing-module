import allure

from tests_graphql.operations.create_order_from_cart.create_order_from_cart_operations import (
    CreateOrderFromCartOperations,
)


@allure.title("Successfull Create Order From Cart (GraphQL)")
def test_create_order_from_cart(graphql_client):
    create_order_from_cart_operations = CreateOrderFromCartOperations(graphql_client)

    create_order_from_cart_operations.add_item_to_cart()
    create_order_from_cart_operations.create_order_from_cart()
