from gql import gql
from graphql_client.types.builder_page_item_type import BuilderPageItemType


class BuilderPageQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> BuilderPageItemType:
        query_string = f"""
            query builderPage($storeId: String!, $pageId: String!) {{
                builderPage(
                    storeId: $storeId,
                    pageId: $pageId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["builderPage"]
