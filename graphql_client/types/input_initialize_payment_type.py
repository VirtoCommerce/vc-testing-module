from pydantic import BaseModel


class InputInitializePaymentType(BaseModel):
    def __init__(self):

        self.orderId: str | None
        self.paymentId: str
