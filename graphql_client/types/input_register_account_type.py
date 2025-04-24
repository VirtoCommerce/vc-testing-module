from pydantic import BaseModel


class InputRegisterAccountType(BaseModel):
    def __init__(self):

        self.username: str
        self.email: str
        self.password: str
