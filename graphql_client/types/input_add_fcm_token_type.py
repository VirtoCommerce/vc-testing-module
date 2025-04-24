from pydantic import BaseModel


class InputAddFcmTokenType(BaseModel):
    def __init__(self):

        self.token: str
