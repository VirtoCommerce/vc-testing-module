from gql import gql
from graphql_client.types.change_organization_logo_result_type import ChangeOrganizationLogoResultType


class ChangeOrganizationLogoMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ChangeOrganizationLogoResultType:
        query_string = f"""
            mutation changeOrganizationLogo($command: InputChangeOrganizationLogoCommandType!) {{
                changeOrganizationLogo(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["changeOrganizationLogo"]
