from gql import gql
from graphql_client.types.category_connection import CategoryConnection


class CategoriesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CategoryConnection:
        query_string = f"""
            query categories($after: String, $first: Int, $storeId: String!, $userId: String, $currencyCode: String, $cultureName: String, $previousOutline: String, $query: String, $filter: String, $fuzzy: Boolean, $fuzzyLevel: Int, $facet: String, $sort: String, $categoryIds: [String]) {{
                categories(
                    after: $after,
                    first: $first,
                    storeId: $storeId,
                    userId: $userId,
                    currencyCode: $currencyCode,
                    cultureName: $cultureName,
                    previousOutline: $previousOutline,
                    query: $query,
                    filter: $filter,
                    fuzzy: $fuzzy,
                    fuzzyLevel: $fuzzyLevel,
                    facet: $facet,
                    sort: $sort,
                    categoryIds: $categoryIds
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["categories"]
