from pydantic import BaseModel


class LoyaltyOperationLog(BaseModel):
    def __init__(self):
        from decimal import Decimal
        from graphql_client.types.loyalty_operation_log_object import LoyaltyOperationLogObject
        from datetime import datetime

        self.id: str
        self.operationType: str
        self.amount: Decimal
        self.createdDate: datetime
        self.object: LoyaltyOperationLogObject | None
