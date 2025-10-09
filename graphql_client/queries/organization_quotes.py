from gql import gql
from graphql_client.types.opus_quote_connection import OpusQuoteConnection


class OrganizationQuotesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> OpusQuoteConnection:
        query_string = f"""
            query organizationQuotes($after: String, $first: Int, $keyword: String, $sort: String, $storeId: String, $userId: String, $currencyCode: String, $cultureName: String, $filter: String, $organizationId: String) {{
                organizationQuotes(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    storeId: $storeId,
                    userId: $userId,
                    currencyCode: $currencyCode,
                    cultureName: $cultureName,
                    filter: $filter,
                    organizationId: $organizationId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["organizationQuotes"]
