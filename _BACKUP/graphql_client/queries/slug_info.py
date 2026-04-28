from gql import gql
from graphql_client.types.slug_info_response_type import SlugInfoResponseType


class SlugInfoQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> SlugInfoResponseType:
        query_string = f"""
            query slugInfo($slug: String, $permalink: String, $storeId: String, $userId: String, $cultureName: String) {{
                slugInfo(
                    slug: $slug,
                    permalink: $permalink,
                    storeId: $storeId,
                    userId: $userId,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["slugInfo"]
