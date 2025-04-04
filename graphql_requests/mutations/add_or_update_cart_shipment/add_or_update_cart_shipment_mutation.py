from gql import Client
from .add_or_update_cart_shipment_body import ADD_OR_UPDATE_CART_SHIPMENT


class AddOrUpdateCartShipmentMutation:
    def __init__(self, graphql_cient: Client):
        self.graphql_client = graphql_cient

    def execute(self, store_id: str, user_id: str, currency_code: str, culture_name: str, shipment):
        variables = {
            "command": {
                "storeId": store_id,
                "userId": user_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
                "shipment": shipment,
            },
        }

        result = self.graphql_client.execute(ADD_OR_UPDATE_CART_SHIPMENT, variable_values=variables)

        return result
