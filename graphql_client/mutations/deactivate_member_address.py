from gql import gql
from graphql_client.types.member_type import MemberType


class DeactivateMemberAddressMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> MemberType:
        query_string = f"""
            mutation deactivateMemberAddress($command: InputDeactivateMemberAddressType!) {{
                deactivateMemberAddress(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["deactivateMemberAddress"]
