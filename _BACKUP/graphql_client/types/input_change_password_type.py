from pydantic import BaseModel


class InputChangePasswordType(BaseModel):
    def __init__(self):

        self.userId: str
        self.oldPassword: str
        self.newPassword: str
