from pydantic import BaseModel


class SupplierTaxCertificateConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.supplier_tax_certificate_type import SupplierTaxCertificateType
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.supplier_tax_certificate_edge import SupplierTaxCertificateEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[SupplierTaxCertificateEdge] | None
        self.items: list[SupplierTaxCertificateType] | None
