from pydantic import BaseModel


class ChangeQuoteItemQuantityCommandType(BaseModel):
    def __init__(self):

        self.quoteId: str
        self.lineItemId: str
        self.quantity: int
