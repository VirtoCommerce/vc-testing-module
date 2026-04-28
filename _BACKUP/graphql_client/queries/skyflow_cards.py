from gql import gql
from graphql_client.types.skyflow_card_response_type import SkyflowCardResponseType


class SkyflowCardsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> SkyflowCardResponseType:
        query_string = f"""
            query skyflowCards($storeId: String) {{
                skyflowCards(
                    storeId: $storeId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["skyflowCards"]
