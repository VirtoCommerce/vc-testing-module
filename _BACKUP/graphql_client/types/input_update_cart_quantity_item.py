from pydantic import BaseModel


class InputUpdateCartQuantityItem(BaseModel):
    def __init__(self):

        self.productId: str
        self.quantity: int
