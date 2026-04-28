from gql import gql
from graphql_client.types.user_type import UserType


class UserQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> UserType:
        query_string = f"""
            query user($id: String, $userName: String, $email: String, $loginProvider: String, $providerKey: String) {{
                user(
                    id: $id,
                    userName: $userName,
                    email: $email,
                    loginProvider: $loginProvider,
                    providerKey: $providerKey
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["user"]
