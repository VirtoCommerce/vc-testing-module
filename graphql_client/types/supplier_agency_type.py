from pydantic import BaseModel


class SupplierAgencyType(BaseModel):
    def __init__(self):
        from graphql_client.types.supplier_agency_in_progress_type import SupplierAgencyInProgressType
        from graphql_client.types.supplier_tax_certificate_connection import SupplierTaxCertificateConnection
        from graphql_client.types.supplier_type import SupplierType
        from graphql_client.types.organization import Organization
        from graphql_client.types.supplier_agency_payment_method_type import SupplierAgencyPaymentMethodType

        self.id: str | None
        self.supplierId: str
        self.agencyId: str
        self.supplierAgencyId: str | None
        self.contractNumber: str | None
        self.leadAgency: str | None
        self.setupStatus: str | None
        self.isGuestAccount: bool
        self.isOrderAllowed: bool
        self.isOrderSetupRequestRequired: bool
        self.supplier: SupplierType
        self.agency: Organization
        self.paymentMethods: list[SupplierAgencyPaymentMethodType]
        self.inProgress: SupplierAgencyInProgressType
        self.taxCertificates: SupplierTaxCertificateConnection | None
