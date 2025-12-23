from pydantic import BaseModel


class LoyaltyOperationLogConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.loyalty_operation_log_edge import LoyaltyOperationLogEdge
        from graphql_client.types.loyalty_operation_log import LoyaltyOperationLog
        from graphql_client.types.page_info import PageInfo

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[LoyaltyOperationLogEdge] | None
        self.items: list[LoyaltyOperationLog] | None
