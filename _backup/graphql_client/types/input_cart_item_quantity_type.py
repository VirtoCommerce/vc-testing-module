from pydantic import BaseModel


class InputCartItemQuantityType(BaseModel):
    def __init__(self):

        self.lineItemId: str
        self.quantity: int
