from pydantic import BaseModel


class InputUpdateWishlistLineItemType(BaseModel):
    def __init__(self):

        self.lineItemId: str
        self.quantity: int
