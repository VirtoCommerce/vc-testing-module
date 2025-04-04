from .remove_cart_address_body import REMOVE_CART_ADDRESS


class RemoveCartAddressMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, store_id: str, user_id: str, address_id: str, currency_code: str, culture_name: str):
        variables = {
            "command": {
                "storeId": store_id,
                "userId": user_id,
                "addressId": address_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
            },
        }

        result = self.graphql_client.execute(REMOVE_CART_ADDRESS, variable_values=variables)

        return result
