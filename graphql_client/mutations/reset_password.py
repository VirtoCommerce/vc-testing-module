from gql import gql


class SendPasswordResetEmailMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, payload: dict) -> bool:
        variables = {"command": payload}
        query_string = f"""
            mutation sendPasswordResetEmail($command: SendPasswordResetEmailCommandType!) {{
                sendPasswordResetEmail(command: $command)
            }}
        """

        return self.graphql_client.execute(gql(query_string), variable_values=variables)["sendPasswordResetEmail"] 