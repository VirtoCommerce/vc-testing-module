from gql import Client
from graphql_requests.queries.order.order_query import OrderQuery


class OrderOperations:
    def __init__(self, auth_token: str, graphql_client: Client):
        self.auth_token = auth_token
        self.graphql_client = graphql_client

    def get_order(self, order_id: str):
        """
        Get order details by ID and perform basic validation.
        Args:
            order_id (str): ID of the order to retrieve
        Returns:
            dict: Validated order data containing items, addresses, and totals
        """

        self.graphql_client.set_headers({"Authorization": f"Bearer {self.auth_token}"})

        order_query = OrderQuery(self.graphql_client)

        result = order_query.execute(order_id)

        return result
