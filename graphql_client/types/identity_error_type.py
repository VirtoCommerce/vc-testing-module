from pydantic import BaseModel


class IdentityErrorType(BaseModel):
    def __init__(self):

        self.code: str | None
        self.description: str | None
