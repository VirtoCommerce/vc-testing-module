from pydantic import BaseModel


class SupplierTaxCertificateType(BaseModel):
    def __init__(self):
        from datetime import datetime
        from graphql_client.types.supplier_type import SupplierType

        self.id: str
        self.taxCertificateId: str
        self.supplierId: str
        self.modifiedBy: str | None
        self.contactName: str | None
        self.modifiedDate: datetime | None
        self.url: str
        self.name: str
        self.contentType: str | None
        self.size: int
        self.displayName: str
        self.supplier: SupplierType | None
