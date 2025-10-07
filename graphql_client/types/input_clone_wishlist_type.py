from pydantic import BaseModel


class InputCloneWishlistType(BaseModel):
    def __init__(self):

        self.storeId: str
        self.userId: str
        self.listId: str
        self.listName: str | None
        self.cultureName: str | None
        self.currencyCode: str | None
        self.scope: str | None
        self.sharingKey: str | None
        self.description: str | None
