from gql import gql
from graphql_client.types.role_type import RoleType


class RoleQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> RoleType:
        query_string = f"""
            query role($roleName: String!) {{
                role(
                    roleName: $roleName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["role"]
