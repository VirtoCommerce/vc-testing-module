from pydantic import BaseModel


class IdentityErrorInfoType(BaseModel):
    def __init__(self):

        self.code: str
        self.parameter: str | None
        self.description: str | None
