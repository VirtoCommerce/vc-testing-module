from pydantic import BaseModel


class InputRemoveWishlistItemsType(BaseModel):
    def __init__(self):

        self.listId: str
        self.lineItemIds: list[str]
