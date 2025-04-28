from gql import gql
from graphql_client.types.user_type import UserType


class MeQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> UserType:
        query_string = f"""
            query me($userId: String) {{
                me(
                    userId: $userId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["me"]
