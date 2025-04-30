from gql import Client
from graphql_client.types.customer_order_type import CustomerOrderType
from tests_graphql.operations.order.fragments.order_fragment import ORDER_FRAGMENT
from graphql_client.queries.order import OrderQuery


class OrderOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def get_order(self, order_id: str) -> CustomerOrderType:
        order_query = OrderQuery(self.graphql_client)

        variables = {"id": order_id}

        result = order_query.execute(variables=variables, return_fields=ORDER_FRAGMENT)

        return result
