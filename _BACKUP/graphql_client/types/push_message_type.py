from pydantic import BaseModel


class PushMessageType(BaseModel):
    def __init__(self):
        from datetime import datetime

        self.id: str
        self.shortMessage: str
        self.createdDate: datetime
        self.isRead: bool
        self.isHidden: bool
