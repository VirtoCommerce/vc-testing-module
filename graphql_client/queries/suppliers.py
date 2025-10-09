from gql import gql
from graphql_client.types.supplier_connection import SupplierConnection


class SuppliersQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> SupplierConnection:
        query_string = f"""
            query suppliers($after: String, $first: Int, $query: String, $categories: [String], $outlineNamed: String, $isActive: Boolean, $isActivePerAgency: Boolean, $isVisibleInCarousel: Boolean, $isConnected: Boolean, $isComingSoon: Boolean, $withFacets: Boolean, $sort: String, $userId: String, $storeId: String!, $supplierIds: [String]) {{
                suppliers(
                    after: $after,
                    first: $first,
                    query: $query,
                    categories: $categories,
                    outlineNamed: $outlineNamed,
                    isActive: $isActive,
                    isActivePerAgency: $isActivePerAgency,
                    isVisibleInCarousel: $isVisibleInCarousel,
                    isConnected: $isConnected,
                    isComingSoon: $isComingSoon,
                    withFacets: $withFacets,
                    sort: $sort,
                    userId: $userId,
                    storeId: $storeId,
                    supplierIds: $supplierIds
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["suppliers"]
