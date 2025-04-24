from pydantic import BaseModel


class PaymentTransactionType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType
        from datetime import datetime

        self.id: str
        self.isProcessed: bool
        self.processedDate: datetime | None
        self.processError: str | None
        self.processAttemptCount: int
        self.requestData: str | None
        self.responseData: str | None
        self.responseCode: str | None
        self.gatewayIpAddress: str | None
        self.type: str | None
        self.status: str | None
        self.note: str | None
        self.amount: MoneyType
