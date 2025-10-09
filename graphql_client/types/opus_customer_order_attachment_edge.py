from pydantic import BaseModel


class OpusCustomerOrderAttachmentEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_customer_order_attachment_type import OpusCustomerOrderAttachmentType

        self.cursor: str
        self.node: OpusCustomerOrderAttachmentType | None
