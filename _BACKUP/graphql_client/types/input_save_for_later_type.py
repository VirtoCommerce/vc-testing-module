from pydantic import BaseModel


class InputSaveForLaterType(BaseModel):
    def __init__(self):

        self.storeId: str
        self.userId: str
        self.cultureName: str | None
        self.currencyCode: str | None
        self.cartId: str
        self.lineItemIds: list[str]
