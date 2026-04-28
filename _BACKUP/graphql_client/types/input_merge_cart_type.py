from pydantic import BaseModel


class InputMergeCartType(BaseModel):
    def __init__(self):

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.secondCartId: str
        self.deleteAfterMerge: bool | None
