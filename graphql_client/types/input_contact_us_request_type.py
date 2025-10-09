from pydantic import BaseModel


class InputContactUsRequestType(BaseModel):
    def __init__(self):

        self.userId: str
        self.orderId: str | None
        self.orderNumber: str | None
        self.firstName: str
        self.lastName: str
        self.email: str
        self.question: str
        self.phone: str | None
        self.note: str | None
