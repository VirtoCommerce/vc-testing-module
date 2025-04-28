from pydantic import BaseModel


class InputChangeCommentType(BaseModel):
    def __init__(self):

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.comment: str | None
