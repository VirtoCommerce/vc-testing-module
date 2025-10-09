from pydantic import BaseModel


class InputUserSignUpRequestType(BaseModel):
    def __init__(self):

        self.firstName: str
        self.lastName: str
        self.email: str
        self.phone: str | None
        self.organizationName: str
