from pydantic import BaseModel


class RegisterAccountType(BaseModel):
    def __init__(self):

        self.id: str
        self.username: str
        self.email: str
        self.status: str | None
        self.createdBy: str | None
