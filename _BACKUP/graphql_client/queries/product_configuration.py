from gql import gql
from graphql_client.types.configuration_query_response_type import ConfigurationQueryResponseType


class ProductConfigurationQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ConfigurationQueryResponseType:
        query_string = f"""
            query productConfiguration($configurableProductId: String!, $storeId: String!, $userId: String, $cultureName: String, $currencyCode: String) {{
                productConfiguration(
                    configurableProductId: $configurableProductId,
                    storeId: $storeId,
                    userId: $userId,
                    cultureName: $cultureName,
                    currencyCode: $currencyCode
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["productConfiguration"]
