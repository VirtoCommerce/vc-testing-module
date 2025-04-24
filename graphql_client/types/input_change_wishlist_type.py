from pydantic import BaseModel


class InputChangeWishlistType(BaseModel):
    def __init__(self):

        self.listId: str
        self.listName: str | None
        self.scope: str | None
        self.description: str | None
        self.cultureName: str | None
