from gql import gql
from graphql_client.types.store_response_type import StoreResponseType


class StoreQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> StoreResponseType:
        query_string = f"""
            query store($storeId: String, $cultureName: String, $domain: String) {{
                store(
                    storeId: $storeId,
                    cultureName: $cultureName,
                    domain: $domain
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["store"]
