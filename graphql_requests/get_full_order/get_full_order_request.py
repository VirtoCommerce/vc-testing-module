from gql import Client
from .get_full_order_body import GET_FULL_ORDER


class GetFullOrderRequest:
    def __init__(self, client: Client):
        self.client = client

    def execute(self, order_id: str) -> dict:
        """
        Execute GetFullOrder query to retrieve detailed order information.

        Args:
            order_id: The ID of the order to retrieve

        Returns:
            dict: The order details including items, addresses, and totals
        """
        variables = {
            "id": order_id
        }
        
        result = self.client.execute(
            GET_FULL_ORDER,
            variable_values=variables
        )
        
        return result 