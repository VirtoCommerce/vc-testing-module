from pydantic import BaseModel


class InputSupplierTaxCertificateType(BaseModel):
    def __init__(self):

        self.supplierId: str
