from pydantic import BaseModel


class InputAddTaxCertificatesType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_tax_certificate_upload_request_type import InputTaxCertificateUploadRequestType

        self.userId: str
        self.taxCertificates: list[InputTaxCertificateUploadRequestType]
