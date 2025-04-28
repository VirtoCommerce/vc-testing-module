from pydantic import BaseModel


class InventoryInfo(BaseModel):
    def __init__(self):
        from datetime import datetime

        self.inStockQuantity: int
        self.reservedQuantity: int
        self.fulfillmentCenterId: str
        self.fulfillmentCenterName: str
        self.allowPreorder: bool
        self.allowBackorder: bool
        self.preorderAvailabilityDate: datetime | None
        self.backorderAvailabilityDate: datetime | None
