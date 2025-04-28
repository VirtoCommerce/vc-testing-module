from pydantic import BaseModel


class InputDeleteFcmTokenType(BaseModel):
    def __init__(self):

        self.token: str
