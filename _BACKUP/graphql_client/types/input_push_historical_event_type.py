from pydantic import BaseModel


class InputPushHistoricalEventType(BaseModel):
    def __init__(self):

        self.storeId: str | None
        self.productId: str | None
        self.productIds: list[str] | None
        self.sessionId: str | None
        self.eventType: str | None
