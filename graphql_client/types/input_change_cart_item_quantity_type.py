from pydantic import BaseModel


class InputChangeCartItemQuantityType(BaseModel):
    def __init__(self):

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.lineItemId: str
        self.quantity: int
