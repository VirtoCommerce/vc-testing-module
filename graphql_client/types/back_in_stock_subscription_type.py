from pydantic import BaseModel


class BackInStockSubscriptionType(BaseModel):
    def __init__(self):

        self.id: str
        self.storeId: str
        self.productId: str
        self.productCode: str | None
        self.productName: str | None
        self.userId: str
        self.memberId: str | None
        self.isActive: bool
