from gql import Client
from .create_order_from_cart_body import CREATE_ORDER_FROM_CART


class CreateOrderFromCartMutation:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def execute(self, cart_id: str):
        variables = {"command": {"cartId": cart_id}}

        result = self.graphql_client.execute(CREATE_ORDER_FROM_CART, variable_values=variables)

        return result
