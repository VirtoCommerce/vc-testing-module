from pydantic import BaseModel


class SupplierAgencyInProgressType(BaseModel):
    def __init__(self):

        self.supplierSetup: bool | None
        self.accountBilling: bool | None
        self.creditCard: bool | None
