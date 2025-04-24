from gql import gql
from graphql_client.types.custom_identity_result_type import CustomIdentityResultType


class ValidatePasswordQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CustomIdentityResultType:
        query_string = f"""
            query validatePassword($password: String!) {{
                validatePassword(
                    password: $password
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["validatePassword"]
