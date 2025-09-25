from pydantic import BaseModel


class InputCreateCartFromWishlistType(BaseModel):
    def __init__(self):

        self.listId: str
