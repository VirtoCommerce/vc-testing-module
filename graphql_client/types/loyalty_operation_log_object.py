from pydantic import BaseModel


class LoyaltyOperationLogObject(BaseModel):
    def __init__(self):

        self.type: str
        self.orderId: str | None
        self.orderNumber: str | None
