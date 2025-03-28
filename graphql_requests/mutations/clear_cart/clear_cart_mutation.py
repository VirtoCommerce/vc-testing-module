from gql import Client
from .clear_cart_body import CLEAR_CART


class ClearCartMutation:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def execute(self, store_id: str, user_id: str, currency_code: str, culture_name: str, skip_query: bool = False):
        variables = {
            "command": {
                "storeId": store_id,
                "userId": user_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
            },
            "skipQuery": skip_query,
        }

        result = self.graphql_client.execute(CLEAR_CART, variable_values=variables)

        return result
