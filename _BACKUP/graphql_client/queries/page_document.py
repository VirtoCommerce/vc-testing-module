from gql import gql
from graphql_client.types.page_document_type import PageDocumentType


class PageDocumentQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> PageDocumentType:
        query_string = f"""
            query pageDocument($id: String!) {{
                pageDocument(
                    id: $id
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["pageDocument"]
