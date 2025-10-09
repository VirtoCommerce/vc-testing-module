from pydantic import BaseModel


class OpusInputPaymentType(BaseModel):
    def __init__(self):

        self.purchaseOrderNumber: str | None
        self.generalLedgerNumber: str | None
        self.requisitionNumber: str | None
        self.requestSetupAccountBillingMethod: bool | None
