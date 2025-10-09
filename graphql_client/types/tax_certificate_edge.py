from pydantic import BaseModel


class TaxCertificateEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.tax_certificate_type import TaxCertificateType

        self.cursor: str
        self.node: TaxCertificateType | None
