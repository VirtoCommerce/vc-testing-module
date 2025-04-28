from pydantic import BaseModel


class ApproveQuoteResultType(BaseModel):
    def __init__(self):

        self.id: str
        self.orderId: str | None
