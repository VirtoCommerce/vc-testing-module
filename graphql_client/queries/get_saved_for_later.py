from gql import gql
from graphql_client.types.cart_type import CartType


class GetSavedForLaterQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CartType:
        query_string = f"""
            query getSavedForLater($storeId: String!, $userId: String!, $organizationId: String, $currencyCode: String, $cultureName: String) {{
                getSavedForLater(
                    storeId: $storeId,
                    userId: $userId,
                    organizationId: $organizationId,
                    currencyCode: $currencyCode,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["getSavedForLater"]
