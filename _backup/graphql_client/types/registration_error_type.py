from pydantic import BaseModel


class RegistrationErrorType(BaseModel):
    def __init__(self):

        self.code: str | None
        self.description: str | None
        self.parameter: str | None
