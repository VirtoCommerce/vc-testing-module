from pydantic import BaseModel


class InputQuoteItemType(BaseModel):
    def __init__(self):

        self.name: str
        self.sku: str | None
        self.quantity: int | None
