from gql import gql
from graphql_client.types.fulfillment_center_type import FulfillmentCenterType


class FulfillmentCenterQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> FulfillmentCenterType:
        query_string = f"""
            query fulfillmentCenter($id: String!) {{
                fulfillmentCenter(
                    id: $id
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["fulfillmentCenter"]
