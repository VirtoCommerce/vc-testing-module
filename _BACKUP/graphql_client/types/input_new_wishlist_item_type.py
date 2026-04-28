from pydantic import BaseModel


class InputNewWishlistItemType(BaseModel):
    def __init__(self):

        self.productId: str
        self.quantity: int | None
