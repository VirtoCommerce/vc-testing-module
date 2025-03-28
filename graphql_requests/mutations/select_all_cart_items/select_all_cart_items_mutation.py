from gql import Client
from .select_all_cart_items_body import SELECT_ALL_CART_ITEMS


class SelectAllCartItemsMutation:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def execute(self, store_id: str, user_id: str, currency_code: str, culture_name: str):
        variables = {
            "command": {
                "storeId": store_id,
                "userId": user_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
            },
        }

        result = self.graphql_client.execute(SELECT_ALL_CART_ITEMS, variable_values=variables)

        return result
