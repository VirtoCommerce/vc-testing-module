from gql import gql
from graphql_client.types.fulfillment_center_connection import FulfillmentCenterConnection


class FulfillmentCentersQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> FulfillmentCenterConnection:
        query_string = f"""
            query fulfillmentCenters($after: String, $first: Int, $storeId: String, $query: String, $sort: String, $fulfillmentCenterIds: [String]) {{
                fulfillmentCenters(
                    after: $after,
                    first: $first,
                    storeId: $storeId,
                    query: $query,
                    sort: $sort,
                    fulfillmentCenterIds: $fulfillmentCenterIds
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["fulfillmentCenters"]
