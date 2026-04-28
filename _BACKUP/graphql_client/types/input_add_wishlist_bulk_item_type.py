from pydantic import BaseModel


class InputAddWishlistBulkItemType(BaseModel):
    def __init__(self):

        self.listIds: list[str]
        self.productId: str
        self.quantity: int | None
