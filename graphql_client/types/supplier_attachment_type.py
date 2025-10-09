from pydantic import BaseModel


class SupplierAttachmentType(BaseModel):
    def __init__(self):
        from datetime import datetime
        from graphql_client.types.supplier_type import SupplierType

        self.id: str
        self.name: str
        self.url: str
        self.contentType: str | None
        self.size: int
        self.supplierId: str
        self.fileDate: datetime
        self.type: str
        self.supplier: SupplierType | None
