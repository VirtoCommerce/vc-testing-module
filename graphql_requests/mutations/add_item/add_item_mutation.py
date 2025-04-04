from gql import Client
from .add_item_body import ADD_ITEM


class AddItemMutation:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def execute(
        self, store_id: str, user_id: str, product_id: str, quantity: int, currency_code: str, culture_name: str
    ):
        variables = {
            "command": {
                "storeId": store_id,
                "userId": user_id,
                "productId": product_id,
                "quantity": quantity,
                "currencyCode": currency_code,
                "cultureName": culture_name,
            }
        }

        result = self.graphql_client.execute(ADD_ITEM, variable_values=variables)

        return result
