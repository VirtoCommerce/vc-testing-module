from pydantic import BaseModel


class InputDeleteSupplierTaxCertificateType(BaseModel):
    def __init__(self):

        self.userId: str
        self.taxCertificateId: str
        self.supplierTaxCertificateId: str
