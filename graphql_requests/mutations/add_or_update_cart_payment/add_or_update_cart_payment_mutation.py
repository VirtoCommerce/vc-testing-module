from gql import Client
from .add_or_update_cart_payment_body import ADD_OR_UPDATE_CART_PAYMENT_BODY


class AddOrUpdateCartPaymentMutation:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def execute(self, store_id: str, user_id: str, currency_code: str, culture_name: str, payment):
        variables = {
            "command": {
                "storeId": store_id,
                "userId": user_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
                "payment": payment,
            },
        }

        result = self.graphql_client.execute(ADD_OR_UPDATE_CART_PAYMENT_BODY, variable_values=variables)

        return result
