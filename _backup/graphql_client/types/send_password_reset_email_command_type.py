from pydantic import BaseModel


class SendPasswordResetEmailCommandType(BaseModel):
    def __init__(self):

        self.storeId: str | None
        self.cultureName: str | None
        self.loginOrEmail: str
        self.urlSuffix: str | None
