from gql import gql
from graphql_client.types.product_connection import ProductConnection


class ProductsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ProductConnection:
        query_string = f"""
            query products($after: String, $first: Int, $storeId: String!, $userId: String, $currencyCode: String, $cultureName: String, $query: String, $filter: String, $preserveUserQuery: Boolean, $facet: String, $fuzzy: Boolean, $fuzzyLevel: Int, $sort: String, $productIds: [String], $selectedAddressId: String, $selectedAddress: String, $custom: String) {{
                products(
                    after: $after,
                    first: $first,
                    storeId: $storeId,
                    userId: $userId,
                    currencyCode: $currencyCode,
                    cultureName: $cultureName,
                    query: $query,
                    filter: $filter,
                    preserveUserQuery: $preserveUserQuery,
                    facet: $facet,
                    fuzzy: $fuzzy,
                    fuzzyLevel: $fuzzyLevel,
                    sort: $sort,
                    productIds: $productIds,
                    selectedAddressId: $selectedAddressId,
                    selectedAddress: $selectedAddress,
                    custom: $custom
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["products"]
