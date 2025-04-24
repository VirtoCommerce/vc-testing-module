from pydantic import BaseModel


class InputMoveWishlistItemType(BaseModel):
    def __init__(self):

        self.listId: str
        self.destinationListId: str
        self.lineItemId: str
