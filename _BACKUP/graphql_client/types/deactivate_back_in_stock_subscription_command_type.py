from pydantic import BaseModel


class DeactivateBackInStockSubscriptionCommandType(BaseModel):
    def __init__(self):

        self.storeId: str
        self.productId: str
