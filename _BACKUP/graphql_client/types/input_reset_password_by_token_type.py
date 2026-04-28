from pydantic import BaseModel


class InputResetPasswordByTokenType(BaseModel):
    def __init__(self):

        self.token: str
        self.userId: str
        self.newPassword: str
