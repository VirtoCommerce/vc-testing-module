from gql import gql
from graphql_client.types.order_approval_request_type import OrderApprovalRequestType


class OrderApprovalRequestQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> OrderApprovalRequestType:
        query_string = f"""
            query orderApprovalRequest($approvalRequestId: String!, $withPrototypes: Boolean) {{
                orderApprovalRequest(
                    approvalRequestId: $approvalRequestId,
                    withPrototypes: $withPrototypes
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["orderApprovalRequest"]
