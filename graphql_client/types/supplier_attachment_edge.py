from pydantic import BaseModel


class SupplierAttachmentEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.supplier_attachment_type import SupplierAttachmentType

        self.cursor: str
        self.node: SupplierAttachmentType | None
