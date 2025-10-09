from pydantic import BaseModel


class OrderApprovalRequestConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.order_approval_request_edge import OrderApprovalRequestEdge
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.order_approval_request_type import OrderApprovalRequestType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[OrderApprovalRequestEdge] | None
        self.items: list[OrderApprovalRequestType] | None
