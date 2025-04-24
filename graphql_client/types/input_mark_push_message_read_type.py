from pydantic import BaseModel


class InputMarkPushMessageReadType(BaseModel):
    def __init__(self):

        self.messageId: str
