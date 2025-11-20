from gql import gql
from graphql_client.types.custom_identity_result_type import CustomIdentityResultType


class ResetPasswordByTokenMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CustomIdentityResultType:
       
        if return_fields is None:
            return_fields = """
                succeeded
                errors {
                    code
                    description
                }
            """
        
        # Wrap variables in command structure to match GraphQL mutation
        variable_values = {"command": variables}
        
        query_string = f"""
            mutation resetPasswordByToken($command: InputResetPasswordByTokenType) {{
                resetPasswordByToken(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variable_values=variable_values)["resetPasswordByToken"]
