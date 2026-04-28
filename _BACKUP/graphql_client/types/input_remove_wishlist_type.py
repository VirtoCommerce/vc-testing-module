from pydantic import BaseModel


class InputRemoveWishlistType(BaseModel):
    def __init__(self):

        self.listId: str
