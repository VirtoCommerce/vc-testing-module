from pydantic import BaseModel


class InputPersonalDataType(BaseModel):
    def __init__(self):

        self.email: str | None
        self.fullName: str | None
        self.firstName: str | None
        self.lastName: str | None
        self.middleName: str | None
