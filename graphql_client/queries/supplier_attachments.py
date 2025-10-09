from gql import gql
from graphql_client.types.supplier_attachment_connection import SupplierAttachmentConnection


class SupplierAttachmentsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> SupplierAttachmentConnection:
        query_string = f"""
            query supplierAttachments($after: String, $first: Int, $keyword: String, $sort: String, $supplierId: String, $fileDate: DateTime, $type: String, $storeId: String!, $userId: String!) {{
                supplierAttachments(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    supplierId: $supplierId,
                    fileDate: $fileDate,
                    type: $type,
                    storeId: $storeId,
                    userId: $userId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["supplierAttachments"]
