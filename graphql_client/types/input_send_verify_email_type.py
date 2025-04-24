from pydantic import BaseModel


class InputSendVerifyEmailType(BaseModel):
    def __init__(self):

        self.storeId: str
        self.languageCode: str | None
        self.email: str | None
        self.userId: str | None
