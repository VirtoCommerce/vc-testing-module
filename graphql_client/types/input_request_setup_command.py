from pydantic import BaseModel


class InputRequestSetupCommand(BaseModel):
    def __init__(self):
        from graphql_client.types.input_supplier_tax_certificate_upload_request_setup_type import InputSupplierTaxCertificateUploadRequestSetupType

        self.userId: str
        self.supplierId: str
        self.accountBillingMethod: bool | None
        self.creditCardMethod: bool | None
        self.taxExempt: bool
        self.notes: str | None
        self.supplierAccountNumber: str | None
        self.taxCertificates: list[InputSupplierTaxCertificateUploadRequestSetupType] | None
