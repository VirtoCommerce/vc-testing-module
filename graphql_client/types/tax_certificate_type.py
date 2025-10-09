from pydantic import BaseModel


class TaxCertificateType(BaseModel):
    def __init__(self):
        from datetime import datetime
        from graphql_client.types.supplier_tax_certificate_type import SupplierTaxCertificateType

        self.id: str
        self.modifiedBy: str | None
        self.contactName: str | None
        self.modifiedDate: datetime | None
        self.url: str
        self.name: str
        self.contentType: str | None
        self.size: int
        self.displayName: str
        self.startDate: datetime | None
        self.expirationDate: datetime | None
        self.isExpired: bool
        self.regions: list[str]
        self.supplierCertificates: list[SupplierTaxCertificateType]
        self.supplierCertificatesCount: int
