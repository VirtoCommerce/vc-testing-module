from pydantic import BaseModel


class BackInStockSubscriptionEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.back_in_stock_subscription_type import BackInStockSubscriptionType

        self.cursor: str
        self.node: BackInStockSubscriptionType | None
