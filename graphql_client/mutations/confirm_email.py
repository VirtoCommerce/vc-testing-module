from gql import gql
from graphql_client.types.custom_identity_result_type import CustomIdentityResultType


class ConfirmEmailMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CustomIdentityResultType:
        default_return_fields = """
                    succeeded
                    errors {
                        code
                        parameter
                        description
                    }
        """

        fields = return_fields or default_return_fields

        query_string = f"""
            mutation confirmEmail($command: InputConfirmEmailType!) {{
                confirmEmail(
                    command: $command
                ) {{
                    {fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["confirmEmail"]
