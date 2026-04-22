from gql import gql
from graphql_client.types.file_upload_scope_options_type import FileUploadScopeOptionsType


class FileUploadOptionsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> FileUploadScopeOptionsType:
        query_string = f"""
            query fileUploadOptions($scope: String) {{
                fileUploadOptions(
                    scope: $scope
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["fileUploadOptions"]
