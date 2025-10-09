from pydantic import BaseModel


class OrderApprovalRequestEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.order_approval_request_type import OrderApprovalRequestType

        self.cursor: str
        self.node: OrderApprovalRequestType | None
