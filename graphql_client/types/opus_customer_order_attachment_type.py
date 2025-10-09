from pydantic import BaseModel


class OpusCustomerOrderAttachmentType(BaseModel):
    def __init__(self):
        from datetime import datetime

        self.id: str
        self.name: str
        self.url: str
        self.orderNumber: str
        self.orderCustomerName: str
        self.orderCreationDate: datetime
        self.orderId: str
