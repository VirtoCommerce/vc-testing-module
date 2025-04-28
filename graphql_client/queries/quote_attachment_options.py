from gql import gql
from graphql_client.types.file_upload_scope_options_type import FileUploadScopeOptionsType


class QuoteAttachmentOptionsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> FileUploadScopeOptionsType:
        query_string = f"""
            query quoteAttachmentOptions() {{
                quoteAttachmentOptions(
                    
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["quoteAttachmentOptions"]
