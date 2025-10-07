from pydantic import BaseModel


class BackInStockSubscriptionConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.back_in_stock_subscription_type import BackInStockSubscriptionType
        from graphql_client.types.back_in_stock_subscription_edge import BackInStockSubscriptionEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[BackInStockSubscriptionEdge] | None
        self.items: list[BackInStockSubscriptionType] | None
