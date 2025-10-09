from gql import gql
from graphql_client.types.agency_user_type import AgencyUserType


class AvailableApproversQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> list[AgencyUserType]:
        query_string = f"""
            query availableApprovers($userId: String!) {{
                availableApprovers(
                    userId: $userId
                )
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["availableApprovers"]
