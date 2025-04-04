from .cart_body import CART


class CartQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, store_id: str, user_id: str, currency_code: str, culture_name: str):
        variables = {
            "storeId": store_id,
            "userId": user_id,
            "currencyCode": currency_code,
            "cultureName": culture_name,
        }

        return self.graphql_client.execute(CART, variable_values=variables)
