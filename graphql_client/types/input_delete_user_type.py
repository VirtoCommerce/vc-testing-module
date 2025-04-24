from pydantic import BaseModel


class InputDeleteUserType(BaseModel):
    def __init__(self):

        self.userNames: list[str]
