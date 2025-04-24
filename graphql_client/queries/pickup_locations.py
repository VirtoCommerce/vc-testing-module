from gql import gql
from graphql_client.types.pickup_location_connection import PickupLocationConnection


class PickupLocationsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> PickupLocationConnection:
        query_string = f"""
            query pickupLocations($after: String, $first: Int, $keyword: String, $sort: String, $storeId: String) {{
                pickupLocations(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    storeId: $storeId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["pickupLocations"]
