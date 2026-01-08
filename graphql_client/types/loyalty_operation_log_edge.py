from pydantic import BaseModel


class LoyaltyOperationLogEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.loyalty_operation_log import LoyaltyOperationLog

        self.cursor: str
        self.node: LoyaltyOperationLog | None
