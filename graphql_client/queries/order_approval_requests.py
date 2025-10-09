from gql import gql
from graphql_client.types.order_approval_request_connection import OrderApprovalRequestConnection


class OrderApprovalRequestsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> OrderApprovalRequestConnection:
        query_string = f"""
            query orderApprovalRequests($after: String, $first: Int, $keyword: String, $sort: String, $storeId: String!, $customerId: String, $filter: String) {{
                orderApprovalRequests(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    storeId: $storeId,
                    customerId: $customerId,
                    filter: $filter
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["orderApprovalRequests"]
