from gql import gql
from graphql_client.types.page_type import PageType


class PageQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> PageType:
        query_string = f"""
            query page($storeId: String!, $cultureName: String, $id: String!) {{
                page(
                    storeId: $storeId,
                    cultureName: $cultureName,
                    id: $id
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["page"]
