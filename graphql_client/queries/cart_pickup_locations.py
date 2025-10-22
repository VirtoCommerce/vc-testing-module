from gql import gql
from graphql_client.types.product_pickup_location_connection import ProductPickupLocationConnection


class CartPickupLocationsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ProductPickupLocationConnection:
        query_string = f"""
            query cartPickupLocations($after: String, $first: Int, $keyword: String, $sort: String, $cartId: String!, $storeId: String!, $cultureName: String!) {{
                cartPickupLocations(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    cartId: $cartId,
                    storeId: $storeId,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["cartPickupLocations"]
