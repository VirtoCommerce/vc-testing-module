from gql import gql
from graphql_client.types.configuration_items_response_type import ConfigurationItemsResponseType


class ConfigurationItemsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ConfigurationItemsResponseType:
        query_string = f"""
            query configurationItems($cartId: String, $lineItemId: String!, $storeId: String!, $currencyCode: String!, $cartType: String, $cartName: String, $userId: String, $cultureName: String) {{
                configurationItems(
                    cartId: $cartId,
                    lineItemId: $lineItemId,
                    storeId: $storeId,
                    currencyCode: $currencyCode,
                    cartType: $cartType,
                    cartName: $cartName,
                    userId: $userId,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["configurationItems"]
