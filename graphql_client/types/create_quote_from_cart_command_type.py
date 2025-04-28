from pydantic import BaseModel


class CreateQuoteFromCartCommandType(BaseModel):
    def __init__(self):

        self.cartId: str
        self.comment: str
