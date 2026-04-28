from gql import gql
from graphql_client.types.product_pickup_location_connection import ProductPickupLocationConnection


class ProductPickupLocationsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ProductPickupLocationConnection:
        query_string = f"""
            query productPickupLocations($after: String, $first: Int, $keyword: String, $sort: String, $productId: String!, $storeId: String!, $cultureName: String!) {{
                productPickupLocations(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    productId: $productId,
                    storeId: $storeId,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["productPickupLocations"]
