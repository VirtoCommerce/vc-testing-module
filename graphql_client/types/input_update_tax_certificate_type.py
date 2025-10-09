from pydantic import BaseModel


class InputUpdateTaxCertificateType(BaseModel):
    def __init__(self):
        from datetime import datetime
        from graphql_client.types.input_supplier_tax_certificate_type import InputSupplierTaxCertificateType

        self.userId: str
        self.taxCertificateId: str
        self.displayName: str
        self.startDate: datetime | None
        self.expirationDate: datetime | None
        self.regions: list[str]
        self.supplierCertificates: list[InputSupplierTaxCertificateType]
