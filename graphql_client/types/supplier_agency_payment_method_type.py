from pydantic import BaseModel


class SupplierAgencyPaymentMethodType(BaseModel):
    def __init__(self):
        from graphql_client.types.payment_method_availability_type import PaymentMethodAvailabilityType

        self.code: str
        self.name: str | None
        self.setupStatus: str | None
        self.orderSetupRequestAllowed: bool
        self.availability: PaymentMethodAvailabilityType
