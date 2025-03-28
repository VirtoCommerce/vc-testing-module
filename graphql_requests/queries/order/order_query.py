from gql import Client
from .order_body import ORDER


class OrderQuery:
    def __init__(self, client: Client):
        self.client = client

    def execute(self, order_id: str) -> dict:
        variables = {"id": order_id}

        result = self.client.execute(ORDER, variable_values=variables)

        return result
