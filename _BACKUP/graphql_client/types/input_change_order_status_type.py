from pydantic import BaseModel


class InputChangeOrderStatusType(BaseModel):
    def __init__(self):

        self.orderId: str
        self.status: str
