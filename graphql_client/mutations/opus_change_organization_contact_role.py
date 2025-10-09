from gql import gql
from graphql_client.types.opus_contact_type import OpusContactType


class OpusChangeOrganizationContactRoleMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> OpusContactType:
        query_string = f"""
            mutation opusChangeOrganizationContactRole($command: OpusInputChangeOrganizationContactRoleType!) {{
                opusChangeOrganizationContactRole(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["opusChangeOrganizationContactRole"]
