from pydantic import BaseModel


class InputDeleteTaxCertificateType(BaseModel):
    def __init__(self):

        self.userId: str
        self.taxCertificateId: str
