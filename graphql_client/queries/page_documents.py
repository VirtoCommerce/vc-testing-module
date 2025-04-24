from gql import gql
from graphql_client.types.page_document_connection import PageDocumentConnection


class PageDocumentsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> PageDocumentConnection:
        query_string = f"""
            query pageDocuments($after: String, $first: Int, $storeId: String!, $keyword: String!, $cultureName: String) {{
                pageDocuments(
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

        return self.graphql_client.execute(gql(query_string), variables)["pageDocuments"]
