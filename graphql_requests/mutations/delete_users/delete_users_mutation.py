from gql import Client
from .delete_users_body import DELETE_USERS


class DeleteUsersMutation:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def execute(self, user_names: list[str]):
        variables = {"command": {"userNames": user_names}}

        result = self.graphql_client.execute(DELETE_USERS, variable_values=variables)

        return result
