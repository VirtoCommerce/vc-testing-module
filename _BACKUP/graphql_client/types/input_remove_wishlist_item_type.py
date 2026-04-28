from pydantic import BaseModel


class InputRemoveWishlistItemType(BaseModel):
    def __init__(self):

        self.listId: str
        self.lineItemId: str | None
        self.productId: str | None
