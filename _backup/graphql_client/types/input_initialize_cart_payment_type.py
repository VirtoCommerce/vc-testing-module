from pydantic import BaseModel


class InputInitializeCartPaymentType(BaseModel):
    def __init__(self):

        self.cartId: str
        self.paymentId: str
