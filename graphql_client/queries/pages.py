from gql import gql
from graphql_client.types.page_connection import PageConnection


class PagesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> PageConnection:
        query_string = f"""
            query pages($after: String, $first: Int, $storeId: String!, $keyword: String!, $cultureName: String) {{
                pages(
                    after: $after,
                    first: $first,
                    storeId: $storeId,
                    keyword: $keyword,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["pages"]
