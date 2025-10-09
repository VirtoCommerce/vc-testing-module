from pydantic import BaseModel


class SupplierAttachmentConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.supplier_attachment_type import SupplierAttachmentType
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.supplier_attachment_edge import SupplierAttachmentEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[SupplierAttachmentEdge] | None
        self.items: list[SupplierAttachmentType] | None
