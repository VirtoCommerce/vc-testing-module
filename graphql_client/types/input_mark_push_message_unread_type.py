from pydantic import BaseModel


class InputMarkPushMessageUnreadType(BaseModel):
    def __init__(self):

        self.messageId: str
