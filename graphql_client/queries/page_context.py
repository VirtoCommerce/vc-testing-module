from gql import gql
from graphql_client.types.page_context_response_type import PageContextResponseType


class PageContextQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> PageContextResponseType:
        query_string = f"""
            query pageContext($domain: String, $cultureName: String, $permalink: String, $organizationId: String, $userId: String, $storeId: String) {{
                pageContext(
                    domain: $domain,
                    cultureName: $cultureName,
                    permalink: $permalink,
                    organizationId: $organizationId,
                    userId: $userId,
                    storeId: $storeId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["pageContext"]
