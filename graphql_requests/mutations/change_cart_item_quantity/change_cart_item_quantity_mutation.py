from gql import Client
from .change_cart_item_quantity_body import CHANGE_CART_ITEM_QUANTITY


class ChangeCartItemQuantityMutation:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def execute(
        self, store_id: str, user_id: str, currency_code: str, culture_name: str, line_item_id: str, quantity: int
    ):
        variables = {
            "command": {
                "storeId": store_id,
                "userId": user_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
                "lineItemId": line_item_id,
                "quantity": quantity,
            },
        }

        result = self.graphql_client.execute(CHANGE_CART_ITEM_QUANTITY, variable_values=variables)

        return result
