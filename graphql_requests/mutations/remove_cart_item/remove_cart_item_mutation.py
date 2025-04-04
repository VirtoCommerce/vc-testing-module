from gql import Client
from .remove_cart_item_body import REMOVE_CART_ITEM


class RemoveCartItemMutation:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def execute(self, store_id: str, user_id: str, currency_code: str, culture_name: str, line_item_id: str):
        variables = {
            "command": {
                "storeId": store_id,
                "userId": user_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
                "lineItemId": line_item_id,
            },
        }

        result = self.graphql_client.execute(REMOVE_CART_ITEM, variable_values=variables)

        return result
