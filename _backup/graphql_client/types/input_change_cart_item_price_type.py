from pydantic import BaseModel


class InputChangeCartItemPriceType(BaseModel):
    def __init__(self):
        from decimal import Decimal

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.lineItemId: str
        self.price: Decimal
