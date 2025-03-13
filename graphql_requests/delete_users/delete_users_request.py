from .delete_users_body import DELETE_USERS

class RequestDeleteUsers:
    def __init__(self, graphql_client):
        self.client = graphql_client

    def execute(
        self,
        user_names
    ):
        variables = {
            "command": {
                "userNames": user_names
            }
        }

        result = self.client.execute(DELETE_USERS, variable_values=variables)

        return result
