from .create_order_from_cart_body import CREATE_ORDER_FROM_CART


class CreateOrderFromCartRequest:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, cart_id):
        variables = {"command": {"cartId": cart_id}}

        result = self.graphql_client.execute(CREATE_ORDER_FROM_CART, variable_values=variables)

        return result
