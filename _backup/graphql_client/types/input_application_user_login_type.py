from pydantic import BaseModel


class InputApplicationUserLoginType(BaseModel):
    def __init__(self):

        self.loginProvider: str
        self.providerKey: str
