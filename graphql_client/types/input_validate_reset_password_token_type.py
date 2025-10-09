from pydantic import BaseModel


class InputValidateResetPasswordTokenType(BaseModel):
    def __init__(self):

        self.userId: str
        self.token: str
