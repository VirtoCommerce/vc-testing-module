from .remove_shipment_body import REMOVE_SHIPMENT


class RemoveShipmentMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, store_id: str, user_id: str, currency_code: str, culture_name: str, shipment_id: str):
        variables = {
            "command": {
                "storeId": store_id,
                "userId": user_id,
                "shipmentId": shipment_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
            },
        }

        result = self.graphql_client.execute(REMOVE_SHIPMENT, variable_values=variables)

        return result
