from gql import gql
from graphql_client.types.opus_customer_order_attachment_connection import OpusCustomerOrderAttachmentConnection


class OrderAttachmentsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> OpusCustomerOrderAttachmentConnection:
        query_string = f"""
            query orderAttachments($after: String, $first: Int, $keyword: String, $sort: String, $storeId: String!, $userId: String) {{
                orderAttachments(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    storeId: $storeId,
                    userId: $userId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["orderAttachments"]
