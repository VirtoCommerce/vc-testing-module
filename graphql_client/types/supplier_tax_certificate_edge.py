from pydantic import BaseModel


class SupplierTaxCertificateEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.supplier_tax_certificate_type import SupplierTaxCertificateType

        self.cursor: str
        self.node: SupplierTaxCertificateType | None
