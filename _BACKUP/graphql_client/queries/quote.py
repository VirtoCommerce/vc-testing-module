from gql import gql
from graphql_client.types.quote_type import QuoteType


class QuoteQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> QuoteType:
        query_string = f"""
            query quote($id: String, $storeId: String, $userId: String, $currencyCode: String, $cultureName: String) {{
                quote(
                    id: $id,
                    storeId: $storeId,
                    userId: $userId,
                    currencyCode: $currencyCode,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["quote"]
