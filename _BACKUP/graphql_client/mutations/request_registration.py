from gql import gql
from graphql_client.types.request_registration_type import RequestRegistrationType


class RequestRegistrationMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> RequestRegistrationType:
        query_string = f"""
            mutation requestRegistration($command: InputRequestRegistrationType!) {{
                requestRegistration(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["requestRegistration"]
