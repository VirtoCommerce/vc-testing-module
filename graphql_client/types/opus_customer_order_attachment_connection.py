from pydantic import BaseModel


class OpusCustomerOrderAttachmentConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_customer_order_attachment_edge import OpusCustomerOrderAttachmentEdge
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.opus_customer_order_attachment_type import OpusCustomerOrderAttachmentType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[OpusCustomerOrderAttachmentEdge] | None
        self.items: list[OpusCustomerOrderAttachmentType] | None
