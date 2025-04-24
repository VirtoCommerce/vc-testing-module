from pydantic import BaseModel


class ActivateBackInStockSubscriptionCommandType(BaseModel):
    def __init__(self):

        self.storeId: str
        self.productId: str
