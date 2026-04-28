from pydantic import BaseModel


class InputAddWishlistItemType(BaseModel):
    def __init__(self):

        self.listId: str
        self.productId: str
        self.quantity: int | None
