from pydantic import BaseModel


class TaxCertificateConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.tax_certificate_type import TaxCertificateType
        from graphql_client.types.tax_certificate_edge import TaxCertificateEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[TaxCertificateEdge] | None
        self.items: list[TaxCertificateType] | None
