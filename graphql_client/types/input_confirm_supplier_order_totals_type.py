from pydantic import BaseModel


class InputConfirmSupplierOrderTotalsType(BaseModel):
    def __init__(self):
        from decimal import Decimal

        self.shipmentAmount: Decimal | None
        self.discountAmount: Decimal | None
        self.feeAmount: Decimal | None
        self.taxAmount: Decimal | None
        self.total: Decimal | None
