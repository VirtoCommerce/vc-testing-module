from pydantic import BaseModel


class InputTaxCertificateUploadRequestType(BaseModel):
    def __init__(self):
        from datetime import datetime

        self.id: str
        self.url: str
        self.name: str
        self.contentType: str
        self.size: int
        self.displayName: str | None
        self.startDate: datetime | None
        self.expirationDate: datetime | None
        self.regions: list[str] | None
        self.supplierIds: list[str]
        self.updateExistingSupplierCertificates: bool | None
