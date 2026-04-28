from gql import gql
from graphql_client.types.contact_type import ContactType


class UnlockOrganizationContactMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ContactType:
        query_string = f"""
            mutation unlockOrganizationContact($command: InputLockUnlockOrganizationContactType!) {{
                unlockOrganizationContact(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["unlockOrganizationContact"]
