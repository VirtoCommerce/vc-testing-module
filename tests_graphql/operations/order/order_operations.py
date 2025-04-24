from gql import Client
from graphql_client.types.customer_order_type import CustomerOrderType
from tests_graphql.operations.order.order_fragment import ORDER_FRAGMENT
from graphql_client.queries.order import OrderQuery


class OrderOperations:
    def __init__(self, auth_token: str, graphql_client: Client):
        self.auth_token = auth_token
        self.graphql_client = graphql_client

    def get_order(self, order_id: str) -> CustomerOrderType:
        self.graphql_client.set_headers({"Authorization": f"Bearer {self.auth_token}"})

        order_query = OrderQuery(self.graphql_client)

        variables = {"id": order_id}

        result = order_query.execute(variables=variables, return_fields=ORDER_FRAGMENT)

        return result
