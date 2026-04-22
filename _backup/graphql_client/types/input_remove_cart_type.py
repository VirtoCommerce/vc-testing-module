from pydantic import BaseModel


class InputRemoveCartType(BaseModel):
    def __init__(self):

        self.cartId: str
        self.userId: str
