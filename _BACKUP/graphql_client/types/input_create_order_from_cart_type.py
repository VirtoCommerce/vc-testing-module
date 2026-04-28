from pydantic import BaseModel


class InputCreateOrderFromCartType(BaseModel):
    def __init__(self):

        self.cartId: str | None
