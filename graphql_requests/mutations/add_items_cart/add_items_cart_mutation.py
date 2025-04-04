from gql import Client
from .add_items_cart_body import ADD_ITEMS_CART


class AddItemsCartMutation:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def execute(self, store_id: str, user_id: str, currency_code: str, culture_name: str, cart_items):
        variables = {
            "command": {
                "storeId": store_id,
                "userId": user_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
                "cartItems": cart_items,
            }
        }

        return self.graphql_client.execute(ADD_ITEMS_CART, variable_values=variables)
