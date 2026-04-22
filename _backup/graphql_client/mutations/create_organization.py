from gql import gql
from graphql_client.types.organization import Organization


class CreateOrganizationMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> Organization:
        query_string = f"""
            mutation createOrganization($command: InputCreateOrganizationType!) {{
                createOrganization(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["createOrganization"]
