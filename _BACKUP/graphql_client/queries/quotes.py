from gql import gql
from graphql_client.types.quote_connection import QuoteConnection


class QuotesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> QuoteConnection:
        query_string = f"""
            query quotes($after: String, $first: Int, $keyword: String, $sort: String, $storeId: String, $userId: String, $currencyCode: String, $cultureName: String, $filter: String) {{
                quotes(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    storeId: $storeId,
                    userId: $userId,
                    currencyCode: $currencyCode,
                    cultureName: $cultureName,
                    filter: $filter
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["quotes"]
