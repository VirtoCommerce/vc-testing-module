from pydantic import BaseModel


class InputAddCouponType(BaseModel):
    def __init__(self):

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.couponCode: str
