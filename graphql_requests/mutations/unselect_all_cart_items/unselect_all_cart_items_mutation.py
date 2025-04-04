from gql import Client
from .unselect_all_cart_items_body import UNSELECT_ALL_CART_ITEMS


class UnselectAllCartItemsMutation:
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

        result = self.graphql_client.execute(UNSELECT_ALL_CART_ITEMS, variable_values=variables)

        return result
