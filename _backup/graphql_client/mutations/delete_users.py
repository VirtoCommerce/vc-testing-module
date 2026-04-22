from gql import gql
from graphql_client.types.identity_result_type import IdentityResultType


class DeleteUsersMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> IdentityResultType:
        query_string = f"""
            mutation deleteUsers($command: InputDeleteUserType!) {{
                deleteUsers(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["deleteUsers"]
