from gql import gql
from graphql_client.types.custom_identity_result_type import CustomIdentityResultType


class ResetPasswordByTokenMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, payload: dict, return_fields: str = None) -> CustomIdentityResultType:
        # Default return fields for CustomIdentityResultType
        if return_fields is None:
            return_fields = """
                succeeded
                errors {
                    code
                    description
                }
            """
        
        variables = {"command": payload}
        query_string = f"""
            mutation resetPasswordByToken($command: InputResetPasswordByTokenType) {{
                resetPasswordByToken(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variable_values=variables)["resetPasswordByToken"]
