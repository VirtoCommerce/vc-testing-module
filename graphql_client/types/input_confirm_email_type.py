from pydantic import BaseModel


class InputConfirmEmailType(BaseModel):
    def __init__(self):

        self.userId: str
        self.token: str
