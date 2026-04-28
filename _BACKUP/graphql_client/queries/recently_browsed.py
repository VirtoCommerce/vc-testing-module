from gql import gql
from graphql_client.types.get_recently_browsed_response_type import GetRecentlyBrowsedResponseType


class RecentlyBrowsedQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> GetRecentlyBrowsedResponseType:
        query_string = f"""
            query recentlyBrowsed($storeId: String!, $cultureName: String, $currencyCode: String, $maxProducts: Int) {{
                recentlyBrowsed(
                    storeId: $storeId,
                    cultureName: $cultureName,
                    currencyCode: $currencyCode,
                    maxProducts: $maxProducts
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["recentlyBrowsed"]
