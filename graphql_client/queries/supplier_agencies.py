from gql import gql
from graphql_client.types.supplier_agency_connection import SupplierAgencyConnection


class SupplierAgenciesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> SupplierAgencyConnection:
        query_string = f"""
            query supplierAgencies($after: String, $first: Int, $query: String, $categories: [String], $isComingSoon: Boolean, $sort: String, $supplierId: String, $userId: String, $storeId: String!) {{
                supplierAgencies(
                    after: $after,
                    first: $first,
                    query: $query,
                    categories: $categories,
                    isComingSoon: $isComingSoon,
                    sort: $sort,
                    supplierId: $supplierId,
                    userId: $userId,
                    storeId: $storeId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["supplierAgencies"]
