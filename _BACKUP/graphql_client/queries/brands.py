from gql import gql
from graphql_client.types.brand_connection import BrandConnection


class BrandsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> BrandConnection:
        query_string = f"""
            query brands($after: String, $first: Int, $storeId: String!, $userId: String, $currencyCode: String, $cultureName: String, $sort: String, $keyword: String) {{
                brands(
                    after: $after,
                    first: $first,
                    storeId: $storeId,
                    userId: $userId,
                    currencyCode: $currencyCode,
                    cultureName: $cultureName,
                    sort: $sort,
                    keyword: $keyword
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["brands"]
