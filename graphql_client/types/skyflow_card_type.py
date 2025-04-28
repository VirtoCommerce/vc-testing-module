from pydantic import BaseModel


class SkyflowCardType(BaseModel):
    def __init__(self):

        self.cardExpiration: str | None
        self.cardNumber: str
        self.cardholderName: str | None
        self.cvv: str | None
        self.expiryMonth: str | None
        self.expiryYear: str | None
        self.skyflowId: str
        self.userId: str
        self.active: bool
