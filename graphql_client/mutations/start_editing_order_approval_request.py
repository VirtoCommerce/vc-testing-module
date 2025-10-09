from gql import gql
from graphql_client.types.opus_cart_type import OpusCartType


class StartEditingOrderApprovalRequestMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> OpusCartType:
        query_string = f"""
            mutation startEditingOrderApprovalRequest($command: InputStartEditingOrderApprovalRequestType!) {{
                startEditingOrderApprovalRequest(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["startEditingOrderApprovalRequest"]
