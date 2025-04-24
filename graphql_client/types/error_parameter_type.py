from pydantic import BaseModel


class ErrorParameterType(BaseModel):
    def __init__(self):

        self.key: str
        self.value: str
